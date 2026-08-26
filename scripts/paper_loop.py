#!/usr/bin/env python3
"""Discover, classify, and queue new survey papers for human review.

The loop is intentionally conservative: it never edits the main survey tables.
It discovers papers, removes duplicates, classifies candidates, runs a second
LLM review (and an adjudication pass on disagreement), then writes reviewable
artifacts.  A scheduled GitHub Action turns those artifacts into a pull request.

Only the Python standard library is required.  With ``ANTHROPIC_API_KEY`` set,
classification uses the Anthropic Messages API.  Without a key, the pipeline
falls back to deterministic keyword classification and marks every candidate as
``needs_review`` rather than pretending that heuristic output is AI-verified.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable, Protocol


ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_ID_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/(?P<id>\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE
)
MARKDOWN_TITLE_RE = re.compile(r"\[\*\*(?P<title>.+?)\*\*\]\([^)]*\)")
SAFE_SLUG_RE = re.compile(r"[^a-z0-9]+")
KST = dt.timezone(dt.timedelta(hours=9), name="KST")


@dataclasses.dataclass(frozen=True)
class Paper:
    paper_id: str
    title: str
    summary: str
    authors: tuple[str, ...]
    published: str
    updated: str
    categories: tuple[str, ...]
    abs_url: str
    pdf_url: str
    query_names: tuple[str, ...] = ()

    @property
    def primary_category(self) -> str:
        return self.categories[0] if self.categories else ""

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class Classification:
    relevant: bool
    section_id: str
    confidence: float
    rationale: str
    summary: str
    evidence: tuple[str, ...]
    needs_full_text: bool
    source: str

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class LoopDecision:
    status: str
    final: Classification
    passes: tuple[Classification, ...]
    disagreement: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "final": self.final.as_dict(),
            "passes": [item.as_dict() for item in self.passes],
            "disagreement": self.disagreement,
        }


class Classifier(Protocol):
    is_llm: bool

    def classify(
        self,
        paper: Paper,
        *,
        mode: str,
        prior: tuple[Classification, ...] = (),
    ) -> Classification:
        """Return a grounded classification for ``paper``."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def configure_utf8_stdio() -> None:
    """Keep international paper metadata printable on Windows consoles."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="backslashreplace")


def parse_iso_datetime(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def normalize_space(value: str) -> str:
    return " ".join(html.unescape(value).split())


def truncate(value: str, limit: int) -> str:
    """Return a single-line value that fits a Slack or report text budget."""
    value = normalize_space(value)
    if len(value) <= limit:
        return value
    return value[: max(1, limit - 1)].rstrip() + "…"


def slack_escape(value: str) -> str:
    """Escape text while leaving Slack link markup under our control."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def normalize_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(char for char in normalized if char.isalnum())


def slugify(value: str, *, max_length: int = 72) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = SAFE_SLUG_RE.sub("-", ascii_text.casefold()).strip("-")
    return (slug[:max_length].rstrip("-") or "paper")


def extract_arxiv_id(url: str) -> str:
    match = ARXIV_ID_RE.search(url)
    if not match:
        return ""
    return match.group("id")


def parse_arxiv_atom(payload: bytes, *, query_name: str = "fixture") -> list[Paper]:
    root = ET.fromstring(payload)
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        id_text = normalize_space(entry.findtext("atom:id", default="", namespaces=ARXIV_NS))
        paper_id = extract_arxiv_id(id_text)
        if not paper_id:
            continue
        links = {
            node.attrib.get("rel", "alternate"): node.attrib.get("href", "")
            for node in entry.findall("atom:link", ARXIV_NS)
        }
        pdf_url = ""
        for node in entry.findall("atom:link", ARXIV_NS):
            if node.attrib.get("title") == "pdf" or node.attrib.get("type") == "application/pdf":
                pdf_url = node.attrib.get("href", "")
                break
        authors = tuple(
            normalize_space(author.findtext("atom:name", default="", namespaces=ARXIV_NS))
            for author in entry.findall("atom:author", ARXIV_NS)
        )
        categories = tuple(
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", ARXIV_NS)
            if category.attrib.get("term")
        )
        papers.append(
            Paper(
                paper_id=paper_id,
                title=normalize_space(entry.findtext("atom:title", default="", namespaces=ARXIV_NS)),
                summary=normalize_space(
                    entry.findtext("atom:summary", default="", namespaces=ARXIV_NS)
                ),
                authors=tuple(author for author in authors if author),
                published=normalize_space(
                    entry.findtext("atom:published", default="", namespaces=ARXIV_NS)
                ),
                updated=normalize_space(
                    entry.findtext("atom:updated", default="", namespaces=ARXIV_NS)
                ),
                categories=categories,
                abs_url=links.get("alternate", id_text) or id_text,
                pdf_url=pdf_url or f"https://arxiv.org/pdf/{paper_id}",
                query_names=(query_name,),
            )
        )
    return papers


def merge_papers(papers: Iterable[Paper]) -> list[Paper]:
    merged: dict[str, Paper] = {}
    for paper in papers:
        existing = merged.get(paper.paper_id)
        if existing is None:
            merged[paper.paper_id] = paper
            continue
        merged[paper.paper_id] = dataclasses.replace(
            existing,
            query_names=tuple(sorted(set(existing.query_names + paper.query_names))),
        )
    return sorted(merged.values(), key=lambda item: item.published, reverse=True)


def request_bytes(url: str, *, attempts: int, timeout: int, user_agent: str) -> bytes:
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(url, headers={"User-Agent": user_agent})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"Request failed after {attempts} attempts: {url}: {last_error}")


def fetch_arxiv(config: dict[str, Any]) -> list[Paper]:
    source = config["source"]
    base_url = source.get("base_url", "https://export.arxiv.org/api/query")
    max_results = int(source.get("max_results_per_query", 25))
    attempts = int(source.get("request_attempts", 3))
    timeout = int(source.get("request_timeout_seconds", 30))
    delay = float(source.get("request_delay_seconds", 3))
    user_agent = source.get(
        "user_agent", "survey-paper-loop/1.0 (+https://github.com/ssmong)"
    )
    collected: list[Paper] = []
    queries = config.get("queries", [])
    for index, query in enumerate(queries):
        params = urllib.parse.urlencode(
            {
                "search_query": query["search_query"],
                "start": 0,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        payload = request_bytes(
            f"{base_url}?{params}", attempts=attempts, timeout=timeout, user_agent=user_agent
        )
        collected.extend(parse_arxiv_atom(payload, query_name=query["name"]))
        if index + 1 < len(queries):
            time.sleep(delay)
    return merge_papers(collected)


def paper_from_dict(value: dict[str, Any]) -> Paper:
    try:
        return Paper(
            paper_id=str(value["paper_id"]),
            title=str(value["title"]),
            summary=str(value.get("summary", "")),
            authors=tuple(str(item) for item in value.get("authors", [])),
            published=str(value.get("published", "")),
            updated=str(value.get("updated", "")),
            categories=tuple(str(item) for item in value.get("categories", [])),
            abs_url=str(value["abs_url"]),
            pdf_url=str(value.get("pdf_url", "")),
            query_names=tuple(str(item) for item in value.get("query_names", [])),
        )
    except (KeyError, TypeError) as error:
        raise ValueError(f"Invalid serialized paper: {error}") from error


def load_fixture(path: Path) -> list[Paper]:
    if path.suffix.casefold() == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or not all(isinstance(item, dict) for item in raw):
            raise ValueError(f"JSON fixture must contain a list of paper objects: {path}")
        return [paper_from_dict(item) for item in raw]
    return parse_arxiv_atom(path.read_bytes(), query_name="fixture")


def collect_known(content_root: Path) -> tuple[set[str], set[str]]:
    known_ids: set[str] = set()
    known_titles: set[str] = set()
    for path in content_root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        known_ids.update(match.group("id") for match in ARXIV_ID_RE.finditer(text))
        known_titles.update(
            normalize_title(match.group("title")) for match in MARKDOWN_TITLE_RE.finditer(text)
        )
        first_heading = next(
            (line[2:].strip() for line in text.splitlines() if line.startswith("# ")), ""
        )
        if first_heading:
            known_titles.add(normalize_title(first_heading))
    return known_ids, known_titles


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(rendered, encoding="utf-8")


def load_feedback(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid feedback JSONL at {path}:{line_number}: {error}") from error
    return records


def prefilter(paper: Paper, config: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    rules = config.get("prefilter", {})
    corpus = f"{paper.title} {paper.summary}".casefold()
    includes = tuple(
        keyword for keyword in rules.get("include_any", []) if keyword.casefold() in corpus
    )
    excludes = tuple(
        keyword for keyword in rules.get("exclude_any", []) if keyword.casefold() in corpus
    )
    minimum_hits = int(rules.get("minimum_include_hits", 1))
    return len(includes) >= minimum_hits and not excludes, includes


def section_map(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(section["id"]): section for section in config["sections"]}


def validate_classification(
    value: dict[str, Any], config: dict[str, Any], *, source: str
) -> Classification:
    required = {
        "relevant",
        "section_id",
        "confidence",
        "rationale",
        "summary",
        "evidence",
        "needs_full_text",
    }
    missing = required - set(value)
    if missing:
        raise ValueError(f"Missing classification fields: {sorted(missing)}")
    relevant = value["relevant"]
    if not isinstance(relevant, bool):
        raise ValueError("relevant must be a boolean")
    section_id = str(value["section_id"])
    valid_sections = set(section_map(config))
    if relevant and section_id not in valid_sections:
        raise ValueError(f"Relevant paper has invalid section_id={section_id!r}")
    if not relevant:
        section_id = "0"
    confidence = float(value["confidence"])
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0 and 1")
    rationale = normalize_space(str(value["rationale"]))
    summary = normalize_space(str(value["summary"]))
    if not rationale or not summary:
        raise ValueError("rationale and summary must not be empty")
    evidence_value = value["evidence"]
    if not isinstance(evidence_value, list) or not all(
        isinstance(item, str) for item in evidence_value
    ):
        raise ValueError("evidence must be a list of strings")
    evidence = tuple(normalize_space(item) for item in evidence_value if normalize_space(item))
    if relevant and not evidence:
        raise ValueError("Relevant classification requires abstract-grounded evidence")
    needs_full_text = value["needs_full_text"]
    if not isinstance(needs_full_text, bool):
        raise ValueError("needs_full_text must be a boolean")
    return Classification(
        relevant=relevant,
        section_id=section_id,
        confidence=confidence,
        rationale=rationale,
        summary=summary,
        evidence=evidence,
        needs_full_text=needs_full_text,
        source=source,
    )


class HeuristicClassifier:
    is_llm = False

    def __init__(self, config: dict[str, Any]):
        self.config = config

    def classify(
        self,
        paper: Paper,
        *,
        mode: str,
        prior: tuple[Classification, ...] = (),
    ) -> Classification:
        del mode, prior
        corpus = f"{paper.title} {paper.summary}".casefold()
        scored: list[tuple[int, str, list[str]]] = []
        for section in self.config["sections"]:
            hits = [
                keyword
                for keyword in section.get("keywords", [])
                if keyword.casefold() in corpus
            ]
            scored.append((len(hits), str(section["id"]), hits))
        score, section_id, hits = max(
            scored, key=lambda item: item[0], default=(0, "0", [])
        )
        relevant = score > 0
        confidence = min(0.69, 0.42 + 0.07 * score) if relevant else 0.55
        return Classification(
            relevant=relevant,
            section_id=section_id if relevant else "0",
            confidence=confidence,
            rationale=(
                f"Keyword fallback matched section {section_id}: {', '.join(hits[:5])}."
                if relevant
                else "No section-specific keyword was found by the deterministic fallback."
            ),
            summary=paper.summary[:320] or paper.title,
            evidence=tuple(hits[:5]),
            needs_full_text=True,
            source="heuristic",
        )


class AnthropicClassifier:
    is_llm = True

    def __init__(
        self,
        config: dict[str, Any],
        *,
        api_key: str,
        feedback: list[dict[str, Any]],
    ):
        self.config = config
        self.api_key = api_key
        llm = config["llm"]
        self.model = os.environ.get("ANTHROPIC_MODEL") or llm["model"]
        self.base_url = os.environ.get("ANTHROPIC_BASE_URL") or llm.get(
            "base_url", "https://api.anthropic.com"
        )
        self.max_tokens = int(llm.get("max_tokens", 800))
        self.attempts = int(llm.get("request_attempts", 3))
        self.timeout = int(llm.get("request_timeout_seconds", 60))
        self.feedback = feedback[-int(llm.get("feedback_examples", 12)) :]

    def _schema(self) -> dict[str, Any]:
        section_ids = ["0", *section_map(self.config).keys()]
        return {
            "type": "object",
            "properties": {
                "relevant": {"type": "boolean"},
                "section_id": {"type": "string", "enum": section_ids},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "rationale": {"type": "string"},
                "summary": {"type": "string"},
                "evidence": {"type": "array", "items": {"type": "string"}},
                "needs_full_text": {"type": "boolean"},
            },
            "required": [
                "relevant",
                "section_id",
                "confidence",
                "rationale",
                "summary",
                "evidence",
                "needs_full_text",
            ],
            "additionalProperties": False,
        }

    def _prompt(
        self, paper: Paper, mode: str, prior: tuple[Classification, ...]
    ) -> str:
        sections = "\n".join(
            f"{section['id']}. {section['name']}: {section['description']}"
            for section in self.config["sections"]
        )
        feedback = "\n".join(
            json.dumps(item, ensure_ascii=False) for item in self.feedback
        ) or "(none yet)"
        prior_text = "\n".join(
            json.dumps(item.as_dict(), ensure_ascii=False) for item in prior
        ) or "(none)"
        mode_instruction = {
            "initial": "Classify independently from the title and abstract.",
            "review": (
                "Act as a skeptical reviewer. Check whether the initial decision is grounded "
                "in the abstract and correct any relevance or section error."
            ),
            "adjudicate": (
                "Adjudicate the disagreement between earlier passes. Prefer needs_full_text=true "
                "and lower confidence when the abstract does not support a firm decision."
            ),
        }.get(mode, "Classify the paper conservatively.")
        return f"""{mode_instruction}

Survey scope: contact-rich dexterous manipulation, VLA, tactile/force-aware
control, learned impedance, dexterous RL, datasets, simulators, teleoperation,
dexterous hardware, and tactile representation models. Reject papers that only
mention robots or AI without a direct connection to this scope.

Available sections:
{sections}

Paper metadata:
- arXiv: {paper.paper_id}
- title: {paper.title}
- authors: {', '.join(paper.authors)}
- categories: {', '.join(paper.categories)}
- published: {paper.published}
- abstract: {paper.summary}

Earlier passes:
{prior_text}

Human review examples (use as calibration, not as facts about this paper):
{feedback}

Rules:
1. Use only the supplied metadata. Do not invent hardware, results, venue, code,
   datasets, or claims absent from the abstract.
2. Evidence items must be short phrases copied or tightly paraphrased from the
   title/abstract.
3. Use section_id "0" when irrelevant.
4. Set needs_full_text=true when the abstract is insufficient to distinguish
   adjacent sections or verify the claimed scope.
5. A high confidence score requires explicit abstract evidence.
6. Write rationale and summary in Korean for the daily review digest. Preserve
   paper titles, model names, datasets, metrics, and other proper nouns.
"""

    def _request(self, prompt: str) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [
                {
                    "name": "classify_paper",
                    "description": "Return the grounded survey classification.",
                    "input_schema": self._schema(),
                }
            ],
            "tool_choice": {"type": "tool", "name": "classify_paper"},
        }
        body = json.dumps(payload).encode("utf-8")
        url = self.base_url.rstrip("/") + "/v1/messages"
        last_error: Exception | None = None
        for attempt in range(self.attempts):
            request = urllib.request.Request(
                url,
                data=body,
                method="POST",
                headers={
                    "content-type": "application/json",
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    decoded = json.loads(response.read().decode("utf-8"))
                for block in decoded.get("content", []):
                    if block.get("type") == "tool_use" and block.get("name") == "classify_paper":
                        return block["input"]
                raise RuntimeError("Anthropic response did not contain classify_paper tool input")
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", "replace")[:800]
                last_error = RuntimeError(f"Anthropic HTTP {error.code}: {detail}")
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as error:
                last_error = error
            if attempt + 1 < self.attempts:
                time.sleep(2**attempt)
        raise RuntimeError(f"Anthropic classification failed: {last_error}")

    def classify(
        self,
        paper: Paper,
        *,
        mode: str,
        prior: tuple[Classification, ...] = (),
    ) -> Classification:
        validation_attempts = int(self.config["llm"].get("validation_attempts", 2))
        last_error: Exception | None = None
        prompt = self._prompt(paper, mode, prior)
        for attempt in range(validation_attempts):
            try:
                return validate_classification(
                    self._request(prompt), self.config, source=f"anthropic:{mode}"
                )
            except (ValueError, RuntimeError) as error:
                last_error = error
                prompt += (
                    "\n\nThe previous response failed validation: "
                    f"{error}. Return a corrected tool input without adding unsupported facts."
                )
                if attempt + 1 < validation_attempts:
                    time.sleep(1)
        raise RuntimeError(f"Could not obtain a valid {mode} classification: {last_error}")


def decide_with_review_loop(
    paper: Paper, classifier: Classifier, config: dict[str, Any]
) -> LoopDecision:
    review_config = config.get("review_loop", {})
    accept_threshold = float(review_config.get("accept_confidence", 0.84))
    reject_threshold = float(review_config.get("reject_confidence", 0.90))
    initial = classifier.classify(paper, mode="initial")
    if not classifier.is_llm:
        return LoopDecision("needs_review", initial, (initial,), False)

    reviewer = classifier.classify(paper, mode="review", prior=(initial,))
    passes: tuple[Classification, ...] = (initial, reviewer)
    agreement = (
        initial.relevant == reviewer.relevant
        and initial.section_id == reviewer.section_id
    )
    final = reviewer
    disagreement = not agreement

    if disagreement and int(review_config.get("max_passes", 3)) >= 3:
        adjudicator = classifier.classify(
            paper, mode="adjudicate", prior=(initial, reviewer)
        )
        passes = (*passes, adjudicator)
        final = adjudicator

    if (
        final.relevant
        and final.confidence >= accept_threshold
        and not final.needs_full_text
        and (agreement or len(passes) == 3)
    ):
        status = "accepted"
    elif not final.relevant and final.confidence >= reject_threshold:
        status = "rejected"
    else:
        status = "needs_review"
    return LoopDecision(status, final, passes, disagreement)


def is_recent(paper: Paper, *, now: dt.datetime, lookback_days: int) -> bool:
    if not paper.published:
        return True
    return parse_iso_datetime(paper.published) >= now - dt.timedelta(days=lookback_days)


def result_record(
    paper: Paper,
    decision: LoopDecision,
    *,
    prefilter_hits: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "paper": paper.as_dict(),
        "decision": decision.as_dict(),
        "prefilter_hits": list(prefilter_hits),
    }


def render_markdown_report(
    *,
    run_id: str,
    stats: dict[str, int],
    results: list[dict[str, Any]],
    config: dict[str, Any],
) -> str:
    sections = section_map(config)
    lines = [
        f"# Paper loop run {run_id}",
        "",
        "> Generated automatically. Verify the original paper before merging any item into the survey.",
        "",
        "## Run summary",
        "",
        f"- Discovered: {stats['discovered']}",
        f"- New after deduplication: {stats['new']}",
        f"- Carried from backlog: {stats['backlog']}",
        f"- Passed keyword prefilter: {stats['prefiltered']}",
        f"- Classified this run: {stats['queued']}",
        f"- Deferred to a later run: {stats['deferred']}",
        f"- AI accepted: {stats['accepted']}",
        f"- Needs human review: {stats['needs_review']}",
        f"- Rejected: {stats['rejected']}",
        "",
    ]
    for status, heading in (
        ("accepted", "AI-accepted candidates"),
        ("needs_review", "Human-review queue"),
        ("rejected", "Rejected candidates"),
    ):
        subset = [item for item in results if item["decision"]["status"] == status]
        lines.extend([f"## {heading}", ""])
        if not subset:
            lines.extend(["_None._", ""])
            continue
        for item in subset:
            paper = item["paper"]
            decision = item["decision"]
            final = decision["final"]
            section = sections.get(final["section_id"], {"name": "Out of scope"})
            lines.extend(
                [
                    f"### [{paper['title']}]({paper['abs_url']})",
                    "",
                    f"- arXiv: `{paper['paper_id']}`",
                    f"- Published: {paper['published'] or 'unknown'}",
                    f"- Authors: {', '.join(paper['authors'][:8])}",
                    f"- Proposed section: {final['section_id']} — {section['name']}",
                    f"- Confidence: {final['confidence']:.2f}",
                    f"- Full text required: {final['needs_full_text']}",
                    f"- Review-loop disagreement: {decision['disagreement']}",
                    f"- Rationale: {final['rationale']}",
                    f"- Summary: {final['summary']}",
                    f"- Evidence: {'; '.join(final['evidence']) or 'none'}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def render_draft(record: dict[str, Any], config: dict[str, Any]) -> str:
    paper = record["paper"]
    decision = record["decision"]
    final = decision["final"]
    section = section_map(config)[final["section_id"]]
    return f"""---
status: ai_candidate
paper_id: "{paper['paper_id']}"
proposed_section: "{final['section_id']}"
confidence: {final['confidence']:.2f}
needs_full_text: {str(final['needs_full_text']).lower()}
---

# {paper['title']}

**Authors:** {', '.join(paper['authors'])}

**Published:** {paper['published']}

**arXiv:** {paper['abs_url']}

**Proposed survey section:** {final['section_id']}. {section['name']}

## Abstract-grounded summary

{final['summary']}

## Why it may belong

{final['rationale']}

## Evidence used by the classifier

{chr(10).join(f'- {item}' for item in final['evidence'])}

## Required human checks

- [ ] Read the full paper and verify the section assignment.
- [ ] Confirm venue, group, hardware, tasks, metrics, code, and weights.
- [ ] Add the paper to the correct table using that section's existing columns.
- [ ] Create or revise the final detailed entry without unsupported claims.
- [ ] Run `python build.py` and inspect the rendered site.
"""


def build_slack_payload(
    report: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    """Build a compact Korean Slack digest from one auditable run report."""
    slack = config.get("slack", {})
    max_papers = max(1, min(int(slack.get("max_papers", 6)), 12))
    sections = section_map(config)
    generated_at = parse_iso_datetime(report["generated_at"]).astimezone(KST)
    stats = report["stats"]
    reviewable = [
        item
        for item in report["results"]
        if item["decision"]["status"] in {"accepted", "needs_review"}
    ][:max_papers]

    summary_text = (
        f"신규 {stats['new']}편 · 선별 {stats['queued']}편 · "
        f"우선 검토 {stats['accepted'] + stats['needs_review']}편"
    )
    blocks: list[dict[str, Any]] = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"연구문헌 모니터링 · {generated_at:%Y-%m-%d}",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*수집*\n{stats['discovered']}편"},
                {
                    "type": "mrkdwn",
                    "text": f"*중복 제거 후 신규*\n{stats['new']}편",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*이번 실행에서 분석*\n{stats['queued']}편",
                },
                {
                    "type": "mrkdwn",
                    "text": (
                        "*판정*\n"
                        f"후보 {stats['accepted']} · 검토 {stats['needs_review']} · "
                        f"제외 {stats['rejected']}"
                    ),
                },
            ],
        },
    ]

    if reviewable:
        blocks.append({"type": "divider"})
    for index, item in enumerate(reviewable, start=1):
        paper = item["paper"]
        decision = item["decision"]
        final = decision["final"]
        section = sections.get(final["section_id"], {"name": "범위 밖"})
        status = "우선 후보" if decision["status"] == "accepted" else "검토 필요"
        evidence = ", ".join(final["evidence"][:3]) or "초록 근거 확인 필요"
        title = slack_escape(truncate(paper["title"], 180))
        summary = slack_escape(truncate(final["summary"], 520))
        rationale = slack_escape(truncate(final["rationale"], 300))
        evidence = slack_escape(truncate(evidence, 220))
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*{index}. <{paper['abs_url']}|{title}>*\n"
                        f"`{status}`  {final['section_id']}. "
                        f"{slack_escape(section['name'])}  ·  신뢰도 {final['confidence']:.2f}\n"
                        f"{summary}\n"
                        f"*선정 근거*  {rationale}\n"
                        f"*초록 근거*  {evidence}"
                    ),
                },
            }
        )
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": (
                            f"arXiv `{paper['paper_id']}` · "
                            f"원문 확인 {'필요' if final['needs_full_text'] else '권장'} · "
                            f"판정 불일치 {'있음' if decision['disagreement'] else '없음'}"
                        ),
                    }
                ],
            }
        )
        if index < len(reviewable):
            blocks.append({"type": "divider"})

    run_url = ""
    server = os.environ.get("GITHUB_SERVER_URL", "").rstrip("/")
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip("/")
    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    if server and repository and run_id:
        run_url = f"{server}/{repository}/actions/runs/{run_id}"
    footer = "LLM 판정은 검토 우선순위를 정하기 위한 결과이며, Wiki 반영 전 원문 확인 필요"
    if run_url:
        footer += f" · <{run_url}|실행 기록>"
    blocks.extend(
        [
            {"type": "divider"},
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": footer}],
            },
        ]
    )
    return {
        "text": f"연구문헌 모니터링 {generated_at:%Y-%m-%d}: {summary_text}",
        "blocks": blocks,
    }


def send_slack_digest(report: dict[str, Any], config: dict[str, Any]) -> bool:
    """Send a digest when configured; return False for intentional skips."""
    slack = config.get("slack", {})
    if not slack.get("enabled", False):
        print("Slack digest disabled in configuration.")
        return False
    if not report["results"] and not slack.get("notify_when_empty", False):
        print("Slack digest skipped: no papers were analyzed in this run.")
        return False
    webhook_env = str(slack.get("webhook_env", "SLACK_WEBHOOK_URL"))
    webhook_url = os.environ.get(webhook_env, "").strip()
    if not webhook_url:
        print(f"Slack digest skipped: {webhook_env} is not configured.")
        return False

    body = json.dumps(build_slack_payload(report, config), ensure_ascii=False).encode(
        "utf-8"
    )
    attempts = max(1, int(slack.get("request_attempts", 3)))
    timeout = max(1, int(slack.get("request_timeout_seconds", 15)))
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            webhook_url,
            data=body,
            method="POST",
            headers={
                "content-type": "application/json; charset=utf-8",
                "user-agent": config["source"]["user_agent"],
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                response_text = response.read().decode("utf-8", "replace").strip()
            if response_text.lower() != "ok":
                raise RuntimeError(f"unexpected Slack response: {response_text[:200]}")
            print("Slack digest sent.")
            return True
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")[:400]
            last_error = RuntimeError(f"Slack HTTP {error.code}: {detail}")
        except (urllib.error.URLError, TimeoutError, RuntimeError) as error:
            last_error = error
        if attempt + 1 < attempts:
            time.sleep(2**attempt)
    raise RuntimeError(f"Slack digest failed after {attempts} attempts: {last_error}")


def make_classifier(
    config: dict[str, Any], *, no_llm: bool, feedback: list[dict[str, Any]]
) -> Classifier:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if no_llm or not api_key:
        return HeuristicClassifier(config)
    return AnthropicClassifier(config, api_key=api_key, feedback=feedback)


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    config_path = (repo_root / args.config).resolve()
    config = load_json(config_path, None)
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a JSON object: {config_path}")
    state_path = (repo_root / args.state).resolve()
    feedback_path = (repo_root / args.feedback).resolve()
    state = load_json(state_path, {"version": 1, "papers": {}, "pending": {}})
    if not isinstance(state, dict):
        raise ValueError(f"State must be a JSON object: {state_path}")
    state_papers = state.setdefault("papers", {})
    if not isinstance(state_papers, dict):
        raise ValueError(f"State field 'papers' must be a JSON object: {state_path}")
    state_pending = state.setdefault("pending", {})
    if not isinstance(state_pending, dict):
        raise ValueError(f"State field 'pending' must be a JSON object: {state_path}")
    feedback = load_feedback(feedback_path)
    reviewed_ids = {str(item.get("paper_id", "")) for item in feedback}
    classifier = make_classifier(config, no_llm=args.no_llm, feedback=feedback)
    now = parse_iso_datetime(args.now) if args.now else utc_now()
    run_id = now.strftime("%Y-%m-%dT%H%M%SZ")

    if args.fixture:
        fixture_path = Path(args.fixture)
        if not fixture_path.is_absolute():
            fixture_path = repo_root / fixture_path
        papers = load_fixture(fixture_path)
    else:
        papers = fetch_arxiv(config)
    papers = merge_papers(papers)
    known_ids, known_titles = collect_known(repo_root / "content")
    known_ids.update(state_papers.keys())
    known_ids.update(reviewed_ids)

    pending: list[tuple[str, Paper, tuple[str, ...]]] = []
    for pending_id, pending_record in state_pending.items():
        if not isinstance(pending_record, dict) or not isinstance(
            pending_record.get("paper"), dict
        ):
            raise ValueError(
                f"Invalid pending paper record for {pending_id!r} in {state_path}"
            )
        paper = paper_from_dict(pending_record["paper"])
        if paper.paper_id != pending_id:
            raise ValueError(
                f"Pending paper key {pending_id!r} does not match {paper.paper_id!r}"
            )
        if paper.paper_id in known_ids or normalize_title(paper.title) in known_titles:
            continue
        keep, hits = prefilter(paper, config)
        if keep:
            pending.append((str(pending_record.get("enqueued_at", "")), paper, hits))
    pending.sort(key=lambda item: (item[0], item[1].published, item[1].paper_id))
    pending_ids = {paper.paper_id for _, paper, _ in pending}

    new_papers = [
        paper
        for paper in papers
        if paper.paper_id not in known_ids
        and paper.paper_id not in pending_ids
        and normalize_title(paper.title) not in known_titles
    ]
    recent = [
        paper
        for paper in new_papers
        if is_recent(
            paper,
            now=now,
            lookback_days=int(config["source"].get("lookback_days", 45)),
        )
    ]

    fresh_eligible: list[tuple[Paper, tuple[str, ...]]] = []
    for paper in recent:
        keep, hits = prefilter(paper, config)
        if keep:
            fresh_eligible.append((paper, hits))
    eligible = [(paper, hits) for _, paper, hits in pending] + fresh_eligible
    max_candidates = int(config.get("max_candidates_per_run", 10))
    if max_candidates < 1:
        raise ValueError("max_candidates_per_run must be at least 1")
    queued = eligible[:max_candidates]
    deferred = eligible[max_candidates:]

    results: list[dict[str, Any]] = []
    for paper, hits in queued:
        try:
            decision = decide_with_review_loop(paper, classifier, config)
        except RuntimeError as error:
            fallback = HeuristicClassifier(config).classify(paper, mode="initial")
            fallback = dataclasses.replace(
                fallback,
                rationale=f"LLM loop failed ({error}); {fallback.rationale}",
                source="heuristic_after_llm_failure",
            )
            decision = LoopDecision("needs_review", fallback, (fallback,), True)
        results.append(result_record(paper, decision, prefilter_hits=hits))

    stats = {
        "discovered": len(papers),
        "new": len(new_papers),
        "backlog": len(pending),
        "prefiltered": len(eligible),
        "queued": len(queued),
        "deferred": len(deferred),
        "accepted": sum(item["decision"]["status"] == "accepted" for item in results),
        "needs_review": sum(
            item["decision"]["status"] == "needs_review" for item in results
        ),
        "rejected": sum(item["decision"]["status"] == "rejected" for item in results),
    }
    report = {
        "run_id": run_id,
        "generated_at": now.isoformat().replace("+00:00", "Z"),
        "classifier": "anthropic" if classifier.is_llm else "heuristic",
        "stats": stats,
        "results": results,
    }

    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return report

    generated_at = report["generated_at"]
    prior_pending = state_pending
    state["pending"] = {
        paper.paper_id: {
            "paper": paper.as_dict(),
            "prefilter_hits": list(hits),
            "enqueued_at": prior_pending.get(paper.paper_id, {}).get(
                "enqueued_at", generated_at
            ),
        }
        for paper, hits in deferred
    }

    if not results:
        write_json(state_path, state)
        if getattr(args, "notify_slack", False):
            send_slack_digest(report, config)
        print(json.dumps(report["stats"], ensure_ascii=False))
        return report

    runs_dir = repo_root / config["output"]["runs_dir"]
    inbox_path = repo_root / config["output"]["latest_report"]
    write_json(runs_dir / f"{run_id}.json", report)
    inbox_path.parent.mkdir(parents=True, exist_ok=True)
    inbox_path.write_text(
        render_markdown_report(run_id=run_id, stats=stats, results=results, config=config),
        encoding="utf-8",
    )

    drafts_root = repo_root / config["output"]["drafts_dir"]
    for record in results:
        if record["decision"]["status"] != "accepted":
            continue
        paper = record["paper"]
        section_id = record["decision"]["final"]["section_id"]
        draft_path = drafts_root / f"section{section_id}" / (
            f"{paper['paper_id']}_{slugify(paper['title'])}.md"
        )
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(render_draft(record, config), encoding="utf-8")

    for record in results:
        paper = record["paper"]
        final = record["decision"]["final"]
        state_papers[paper["paper_id"]] = {
            "title": paper["title"],
            "status": record["decision"]["status"],
            "section_id": final["section_id"],
            "confidence": final["confidence"],
            "first_seen": generated_at,
            "run_id": run_id,
        }
    write_json(state_path, state)
    if getattr(args, "notify_slack", False):
        send_slack_digest(report, config)
    print(json.dumps(report["stats"], ensure_ascii=False))
    return report


def record_review(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    config_path = (repo_root / args.config).resolve()
    config = load_json(config_path, None)
    if not isinstance(config, dict):
        raise ValueError(f"Config must be a JSON object: {config_path}")
    valid_sections = set(section_map(config))
    if args.decision == "accept" and args.section_id not in valid_sections:
        raise ValueError(
            f"Accepted review requires a valid --section-id; choose from "
            f"{', '.join(sorted(valid_sections, key=int))}"
        )
    feedback_path = (repo_root / args.feedback).resolve()
    record = {
        "paper_id": args.paper_id,
        "decision": args.decision,
        "section_id": args.section_id if args.decision == "accept" else "0",
        "note": args.note,
        "reviewed_at": utc_now().isoformat().replace("+00:00", "Z"),
    }
    feedback_path.parent.mkdir(parents=True, exist_ok=True)
    with feedback_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    repo_default = str(Path(__file__).resolve().parents[1])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=repo_default)
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="Run one discovery/classification cycle")
    run.add_argument("--config", default="automation/paper-loop.json")
    run.add_argument("--state", default="automation/state.json")
    run.add_argument("--feedback", default="automation/review_decisions.jsonl")
    run.add_argument("--fixture", help="Use an offline Atom XML or JSON fixture")
    run.add_argument("--now", help="Override current UTC time (ISO-8601) for tests")
    run.add_argument("--no-llm", action="store_true", help="Force deterministic fallback")
    run.add_argument("--dry-run", action="store_true", help="Print output without writing files")
    run.add_argument(
        "--notify-slack",
        action="store_true",
        help="Send the run digest through the configured Slack webhook",
    )
    run.set_defaults(func=run_pipeline)

    review = subparsers.add_parser("review", help="Record a human feedback example")
    review.add_argument("--config", default="automation/paper-loop.json")
    review.add_argument("--feedback", default="automation/review_decisions.jsonl")
    review.add_argument("--paper-id", required=True)
    review.add_argument("--decision", choices=("accept", "reject"), required=True)
    review.add_argument("--section-id", default="0")
    review.add_argument("--note", default="")
    review.set_defaults(func=record_review)
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_utf8_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (ValueError, RuntimeError, ET.ParseError, OSError) as error:
        print(f"paper-loop error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
