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
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable, Protocol


ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_ID_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/(?P<id>\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE
)
MARKDOWN_TITLE_RE = re.compile(r"\[\*\*(?P<title>.+?)\*\*\]\([^)]*\)")
SAFE_SLUG_RE = re.compile(r"[^a-z0-9]+")
SOURCE_LOCATOR_RE = re.compile(r"\[L\d{4}\]")
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


class ArxivHTMLTextExtractor(HTMLParser):
    """Extract readable paper text from arXiv HTML without external packages."""

    block_tags = {
        "article",
        "blockquote",
        "br",
        "caption",
        "div",
        "figcaption",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "p",
        "section",
        "td",
        "th",
        "tr",
    }
    ignored_tags = {"script", "style", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag in self.ignored_tags:
            self.ignored_depth += 1
        elif not self.ignored_depth and tag in self.block_tags:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.ignored_tags and self.ignored_depth:
            self.ignored_depth -= 1
        elif not self.ignored_depth and tag in self.block_tags:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        lines: list[str] = []
        for raw_line in "".join(self.parts).splitlines():
            line = normalize_space(raw_line)
            if line and (not lines or lines[-1] != line):
                lines.append(line)
        return "\n".join(lines)


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


def extract_arxiv_html_text(payload: bytes) -> str:
    parser = ArxivHTMLTextExtractor()
    parser.feed(payload.decode("utf-8", "replace"))
    parser.close()
    return parser.text()


def number_source_lines(text: str, *, max_chars: int) -> str:
    """Attach stable evidence locators and cap model input size by whole lines."""
    numbered: list[str] = []
    consumed = 0
    for index, raw_line in enumerate(text.splitlines(), start=1):
        line = normalize_space(raw_line)
        if not line:
            continue
        item = f"[L{index:04d}] {line}"
        if numbered and consumed + len(item) + 1 > max_chars:
            break
        numbered.append(item)
        consumed += len(item) + 1
    return "\n".join(numbered)


def fetch_analysis_source(
    paper: Paper, config: dict[str, Any]
) -> tuple[str, str, str]:
    """Return source kind, URL, and numbered text; fall back safely to abstract."""
    analysis = config.get("analysis", {})
    source = config["source"]
    versioned_id = paper.abs_url.rstrip("/").rsplit("/", 1)[-1] or paper.paper_id
    html_url = f"https://arxiv.org/html/{versioned_id}"
    try:
        payload = request_bytes(
            html_url,
            attempts=max(1, int(analysis.get("source_request_attempts", 2))),
            timeout=max(1, int(analysis.get("source_request_timeout_seconds", 30))),
            user_agent=source["user_agent"],
        )
        text = extract_arxiv_html_text(payload)
        if len(text) >= int(analysis.get("minimum_full_text_chars", 4000)):
            return (
                "arxiv_html",
                html_url,
                number_source_lines(
                    text, max_chars=int(analysis.get("max_source_chars", 50000))
                ),
            )
    except RuntimeError:
        pass

    abstract = (
        f"Title: {paper.title}\nAuthors: {', '.join(paper.authors)}\n"
        f"Abstract: {paper.summary}"
    )
    return (
        "abstract",
        paper.abs_url,
        number_source_lines(
            abstract, max_chars=int(analysis.get("max_source_chars", 50000))
        ),
    )


def validate_insight(
    value: dict[str, Any], *, source_kind: str, source_url: str
) -> dict[str, Any]:
    """Validate grounded insight output and calculate comparable deltas in code."""
    if not isinstance(value, dict):
        raise ValueError("Insight output must be a JSON object")
    insight: dict[str, Any] = {}
    for key in ("problem", "method", "contribution", "gap_candidate"):
        text = normalize_space(str(value.get(key, "")))
        if not text:
            raise ValueError(f"Insight field {key!r} must not be empty")
        insight[key] = text

    limitations = value.get("limitations", [])
    evidence = value.get("evidence", [])
    comparisons = value.get("comparisons", [])
    if not isinstance(limitations, list) or not isinstance(evidence, list):
        raise ValueError("Insight limitations and evidence must be arrays")
    if not isinstance(comparisons, list):
        raise ValueError("Insight comparisons must be an array")
    insight["limitations"] = [
        normalize_space(str(item)) for item in limitations[:4] if str(item).strip()
    ]
    insight["evidence"] = [
        normalize_space(str(item)) for item in evidence[:8] if str(item).strip()
    ]
    if not insight["evidence"] or any(
        not SOURCE_LOCATOR_RE.search(item) for item in insight["evidence"]
    ):
        raise ValueError("Every insight must include numbered [L####] evidence")

    checked_comparisons: list[dict[str, Any]] = []
    required = (
        "task",
        "dataset",
        "metric",
        "proposed_value",
        "baseline_name",
        "baseline_value",
        "unit",
        "higher_is_better",
        "conditions_match",
        "comparison_note",
        "proposed_evidence",
        "baseline_evidence",
    )
    for raw in comparisons[:6]:
        if not isinstance(raw, dict) or any(key not in raw for key in required):
            raise ValueError("Each comparison must contain every required field")
        current = float(raw["proposed_value"])
        baseline = float(raw["baseline_value"])
        if not isinstance(raw["conditions_match"], bool):
            raise ValueError("conditions_match must be boolean")
        conditions_match = raw["conditions_match"]
        higher_is_better = raw["higher_is_better"]
        if higher_is_better is not None and not isinstance(higher_is_better, bool):
            raise ValueError("higher_is_better must be true, false, or null")
        proposed_locator = SOURCE_LOCATOR_RE.search(str(raw["proposed_evidence"]))
        baseline_locator = SOURCE_LOCATOR_RE.search(str(raw["baseline_evidence"]))
        if not proposed_locator or not baseline_locator:
            raise ValueError("Comparison evidence must include numbered [L####] locators")
        absolute_delta: float | None = None
        relative_improvement: float | None = None
        if conditions_match:
            absolute_delta = current - baseline
            if higher_is_better is not None and baseline != 0:
                signed_gain = current - baseline if higher_is_better else baseline - current
                relative_improvement = signed_gain / abs(baseline) * 100
        checked_comparisons.append(
            {
                "task": normalize_space(str(raw["task"])),
                "dataset": normalize_space(str(raw["dataset"])),
                "metric": normalize_space(str(raw["metric"])),
                "proposed_value": current,
                "baseline_name": normalize_space(str(raw["baseline_name"])),
                "baseline_value": baseline,
                "unit": normalize_space(str(raw["unit"])),
                "higher_is_better": higher_is_better,
                "conditions_match": conditions_match,
                "comparison_note": normalize_space(str(raw["comparison_note"])),
                "proposed_evidence": normalize_space(str(raw["proposed_evidence"])),
                "baseline_evidence": normalize_space(str(raw["baseline_evidence"])),
                "absolute_delta": absolute_delta,
                "relative_improvement_percent": relative_improvement,
            }
        )
    insight["comparisons"] = checked_comparisons
    insight["source_kind"] = source_kind
    insight["source_url"] = source_url
    return insight


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


class AnthropicInsightAnalyzer:
    """Extract full-text-grounded research insights for the daily digest."""

    def __init__(self, config: dict[str, Any], *, api_key: str):
        self.config = config
        self.api_key = api_key
        llm = config["llm"]
        analysis = config.get("analysis", {})
        self.model = os.environ.get("ANTHROPIC_MODEL") or llm["model"]
        self.base_url = os.environ.get("ANTHROPIC_BASE_URL") or llm.get(
            "base_url", "https://api.anthropic.com"
        )
        self.max_tokens = int(analysis.get("max_tokens", 1800))
        self.attempts = int(analysis.get("request_attempts", 3))
        self.timeout = int(analysis.get("request_timeout_seconds", 90))

    @staticmethod
    def _schema() -> dict[str, Any]:
        comparison = {
            "type": "object",
            "properties": {
                "task": {"type": "string"},
                "dataset": {"type": "string"},
                "metric": {"type": "string"},
                "proposed_value": {"type": "number"},
                "baseline_name": {"type": "string"},
                "baseline_value": {"type": "number"},
                "unit": {"type": "string"},
                "higher_is_better": {"type": ["boolean", "null"]},
                "conditions_match": {"type": "boolean"},
                "comparison_note": {"type": "string"},
                "proposed_evidence": {"type": "string"},
                "baseline_evidence": {"type": "string"},
            },
            "required": [
                "task",
                "dataset",
                "metric",
                "proposed_value",
                "baseline_name",
                "baseline_value",
                "unit",
                "higher_is_better",
                "conditions_match",
                "comparison_note",
                "proposed_evidence",
                "baseline_evidence",
            ],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {
                "problem": {"type": "string"},
                "method": {"type": "string"},
                "contribution": {"type": "string"},
                "limitations": {"type": "array", "items": {"type": "string"}},
                "gap_candidate": {"type": "string"},
                "comparisons": {"type": "array", "items": comparison},
                "evidence": {"type": "array", "items": {"type": "string"}},
            },
            "required": [
                "problem",
                "method",
                "contribution",
                "limitations",
                "gap_candidate",
                "comparisons",
                "evidence",
            ],
            "additionalProperties": False,
        }

    @staticmethod
    def _prompt(
        paper: Paper, *, source_kind: str, source_url: str, source_text: str
    ) -> str:
        return f"""다음 논문을 매일 아침 연구자가 빠르게 검토할 수 있도록 분석하라.

Paper: {paper.title}
arXiv: {paper.paper_id}
Source kind: {source_kind}
Source URL: {source_url}

규칙:
1. 모든 서술은 제공된 번호가 있는 source에서만 도출한다. 논문에 없는 주장,
   수치, 데이터셋, 한계, 선행연구를 만들지 않는다.
2. problem은 해결하려는 구체적 문제, method는 실제 접근, contribution은 기존
   접근과 비교해 무엇이 달라졌는지를 한국어로 간결하게 작성한다.
3. gap_candidate는 후속 연구 후보일 뿐 확정된 연구 공백으로 단정하지 않는다.
   저자가 명시한 limitation이나 실험 범위의 경계에서만 도출한다.
4. comparisons에는 source에 제안법과 baseline의 숫자가 모두 명시된 경우만
   넣는다. task, dataset, metric, 평가 조건이 같아야 conditions_match=true다.
   조건이 다르면 false로 두고 comparison_note에 차이를 적는다.
5. absolute/relative delta는 계산하지 않는다. 원 수치만 반환하면 코드가 다시
   계산한다. higher_is_better를 source로 판단할 수 없으면 null로 둔다.
6. proposed_evidence와 baseline_evidence에는 반드시 [L####] 위치를 넣는다.
   evidence에도 핵심 판단을 뒷받침하는 line 위치와 짧은 근거를 적는다.
7. source_kind가 abstract면 comparisons는 빈 배열로 두고, 원문 확인이 필요한
   내용은 단정하지 않는다.

Numbered source:
{source_text}
"""

    def analyze(
        self, paper: Paper, *, source_kind: str, source_url: str, source_text: str
    ) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": self._prompt(
                        paper,
                        source_kind=source_kind,
                        source_url=source_url,
                        source_text=source_text,
                    ),
                }
            ],
            "tools": [
                {
                    "name": "analyze_paper",
                    "description": "Return grounded research insights and comparisons.",
                    "input_schema": self._schema(),
                }
            ],
            "tool_choice": {"type": "tool", "name": "analyze_paper"},
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
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
                    if block.get("type") == "tool_use" and block.get("name") == "analyze_paper":
                        return validate_insight(
                            block["input"],
                            source_kind=source_kind,
                            source_url=source_url,
                        )
                raise RuntimeError("Anthropic response did not contain analyze_paper tool input")
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", "replace")[:800]
                last_error = RuntimeError(f"Anthropic HTTP {error.code}: {detail}")
            except (
                urllib.error.URLError,
                TimeoutError,
                json.JSONDecodeError,
                RuntimeError,
                TypeError,
                ValueError,
            ) as error:
                last_error = error
            if attempt + 1 < self.attempts:
                time.sleep(2**attempt)
        raise RuntimeError(f"Anthropic insight analysis failed: {last_error}")


def enrich_results_with_insights(
    results: list[dict[str, Any]], config: dict[str, Any]
) -> None:
    """Add bounded full-text analysis to the highest-priority review records."""
    analysis = config.get("analysis", {})
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not analysis.get("enabled", False) or not api_key:
        return
    analyzer = AnthropicInsightAnalyzer(config, api_key=api_key)
    limit = max(1, int(analysis.get("max_papers_per_run", 4)))
    reviewable = [
        item
        for item in results
        if item["decision"]["status"] in {"accepted", "needs_review"}
    ][:limit]
    for record in reviewable:
        paper = paper_from_dict(record["paper"])
        try:
            source_kind, source_url, source_text = fetch_analysis_source(paper, config)
            record["insight"] = analyzer.analyze(
                paper,
                source_kind=source_kind,
                source_url=source_url,
                source_text=source_text,
            )
        except RuntimeError as error:
            record["insight_error"] = truncate(str(error), 600)


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


def format_metric_value(value: float, unit: str) -> str:
    magnitude = abs(value)
    if magnitude and (magnitude >= 10000 or magnitude < 0.001):
        rendered = f"{value:.3g}"
    else:
        rendered = f"{value:.4f}".rstrip("0").rstrip(".")
    return f"{rendered}{unit}" if unit in {"%", "°"} else f"{rendered} {unit}".strip()


def format_comparison(comparison: dict[str, Any]) -> str:
    current = format_metric_value(comparison["proposed_value"], comparison["unit"])
    baseline = format_metric_value(comparison["baseline_value"], comparison["unit"])
    prefix = f"{comparison['metric']}: {current} vs {comparison['baseline_name']} {baseline}"
    if not comparison["conditions_match"]:
        return f"{prefix} · 비교 보류({comparison['comparison_note']})"
    relative = comparison.get("relative_improvement_percent")
    if relative is None:
        return f"{prefix} · 절대 차이 {comparison['absolute_delta']:+.4g}"
    return f"{prefix} · 상대 개선 {relative:+.1f}%"


def render_insight_markdown(record: dict[str, Any]) -> str:
    insight = record.get("insight")
    if not insight:
        error = record.get("insight_error")
        return f"\n## Full-text analysis\n\nAnalysis unavailable: {error}\n" if error else ""
    comparison_lines = (
        "\n".join(f"- {format_comparison(item)}" for item in insight["comparisons"])
        or "- No directly comparable numeric result was extracted."
    )
    limitation_lines = (
        "\n".join(f"- {item}" for item in insight["limitations"])
        or "- No explicit limitation was extracted from the available source."
    )
    evidence_lines = (
        "\n".join(f"- {item}" for item in insight["evidence"])
        or "- No additional evidence locator was returned."
    )
    return f"""
## Grounded research insight

**Problem:** {insight['problem']}

**Method:** {insight['method']}

**Contribution over prior work:** {insight['contribution']}

**Gap candidate:** {insight['gap_candidate']}

### Reported numeric comparisons

{comparison_lines}

### Limitations

{limitation_lines}

### Evidence locators

{evidence_lines}

**Analysis source:** [{insight['source_kind']}]({insight['source_url']})
"""


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
                ]
            )
            if item.get("insight"):
                insight = item["insight"]
                lines.extend(
                    [
                        f"- Problem: {insight['problem']}",
                        f"- Method: {insight['method']}",
                        f"- Contribution: {insight['contribution']}",
                        f"- Gap candidate: {insight['gap_candidate']}",
                        f"- Analysis source: {insight['source_kind']} ({insight['source_url']})",
                    ]
                )
                lines.extend(
                    f"  - Comparison: {format_comparison(comparison)}"
                    for comparison in insight["comparisons"]
                )
            elif item.get("insight_error"):
                lines.append(f"- Full-text analysis error: {item['insight_error']}")
            lines.append("")
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

{render_insight_markdown(record)}

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
        insight = item.get("insight")
        if insight:
            comparisons = [
                slack_escape(truncate(format_comparison(comparison), 300))
                for comparison in insight["comparisons"][:2]
            ]
            comparison_text = (
                "\n".join(f"• {comparison}" for comparison in comparisons)
                if comparisons
                else "직접 비교 가능한 동일 조건 수치 없음"
            )
            detail_text = (
                f"*문제*  {slack_escape(truncate(insight['problem'], 300))}\n"
                f"*방법*  {slack_escape(truncate(insight['method'], 300))}\n"
                f"*기여*  {slack_escape(truncate(insight['contribution'], 360))}\n"
                f"*Gap 후보*  {slack_escape(truncate(insight['gap_candidate'], 300))}\n"
                f"*정량 비교(논문 보고값)*\n{comparison_text}"
            )
        else:
            detail_text = (
                f"{summary}\n"
                f"*선정 근거*  {rationale}\n"
                f"*초록 근거*  {evidence}"
            )
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*{index}. <{paper['abs_url']}|{title}>*\n"
                        f"`{status}`  {final['section_id']}. "
                        f"{slack_escape(section['name'])}  ·  신뢰도 {final['confidence']:.2f}\n"
                        f"{detail_text}"
                    ),
                },
            }
        )
        source_note = ""
        if insight:
            source_note = (
                f" · <{insight['source_url']}|분석 원문({insight['source_kind']})>"
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
                            f"{source_note}"
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

    if classifier.is_llm and not args.no_llm:
        enrich_results_with_insights(results, config)

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
