from __future__ import annotations

import argparse
import contextlib
import dataclasses
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import paper_loop


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "arxiv_sample.xml"
CONFIG = json.loads(
    (REPO_ROOT / "automation" / "paper-loop.json").read_text(encoding="utf-8")
)


def classification(
    *,
    relevant: bool = True,
    section_id: str = "5",
    confidence: float = 0.95,
    needs_full_text: bool = False,
    source: str = "fake",
) -> paper_loop.Classification:
    return paper_loop.Classification(
        relevant=relevant,
        section_id=section_id if relevant else "0",
        confidence=confidence,
        rationale="The abstract directly supports the decision.",
        summary="A grounded test summary.",
        evidence=("variable impedance",) if relevant else (),
        needs_full_text=needs_full_text,
        source=source,
    )


class SequenceClassifier:
    is_llm = True

    def __init__(self, outputs: list[paper_loop.Classification]):
        self.outputs = iter(outputs)
        self.modes: list[str] = []

    def classify(self, paper, *, mode, prior=()):
        del paper, prior
        self.modes.append(mode)
        return next(self.outputs)


class PaperParsingTests(unittest.TestCase):
    def test_parse_atom_normalizes_metadata(self):
        papers = paper_loop.parse_arxiv_atom(
            FIXTURE.read_bytes(), query_name="offline-test"
        )

        self.assertEqual(len(papers), 3)
        first = papers[0]
        self.assertEqual(first.paper_id, "2608.00001")
        self.assertEqual(
            first.title, "Tactile Dexterous Manipulation with Variable Impedance"
        )
        self.assertEqual(first.authors, ("Ada Researcher", "Min Robotist"))
        self.assertEqual(first.categories, ("cs.RO",))
        self.assertEqual(first.query_names, ("offline-test",))
        self.assertEqual(first.pdf_url, "https://arxiv.org/pdf/2608.00001v1")

    def test_merge_combines_query_provenance(self):
        paper = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes(), query_name="one")[0]
        duplicate = dataclasses.replace(paper, query_names=("two",))

        merged = paper_loop.merge_papers([paper, duplicate])

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0].query_names, ("one", "two"))

    def test_collect_known_finds_arxiv_ids_and_titles(self):
        with tempfile.TemporaryDirectory() as directory:
            content = Path(directory)
            (content / "known.md").write_text(
                "# Heading Paper\n\n[**Table Paper**](https://arxiv.org/abs/2608.12345v2)\n",
                encoding="utf-8",
            )

            ids, titles = paper_loop.collect_known(content)

        self.assertEqual(ids, {"2608.12345"})
        self.assertIn(paper_loop.normalize_title("Heading Paper"), titles)
        self.assertIn(paper_loop.normalize_title("Table Paper"), titles)


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.paper = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())[0]

    def test_validate_rejects_unsupported_section(self):
        value = classification().as_dict()
        value.pop("source")
        value["section_id"] = "99"

        with self.assertRaisesRegex(ValueError, "invalid section_id"):
            paper_loop.validate_classification(value, CONFIG, source="test")

    def test_review_loop_accepts_two_grounded_agreeing_passes(self):
        classifier = SequenceClassifier(
            [classification(source="initial"), classification(source="review")]
        )

        decision = paper_loop.decide_with_review_loop(self.paper, classifier, CONFIG)

        self.assertEqual(decision.status, "accepted")
        self.assertFalse(decision.disagreement)
        self.assertEqual(classifier.modes, ["initial", "review"])

    def test_review_loop_adjudicates_disagreement(self):
        classifier = SequenceClassifier(
            [
                classification(section_id="5", source="initial"),
                classification(section_id="7", source="review"),
                classification(section_id="5", confidence=0.91, source="adjudicate"),
            ]
        )

        decision = paper_loop.decide_with_review_loop(self.paper, classifier, CONFIG)

        self.assertEqual(decision.status, "accepted")
        self.assertTrue(decision.disagreement)
        self.assertEqual(len(decision.passes), 3)
        self.assertEqual(classifier.modes, ["initial", "review", "adjudicate"])

    def test_heuristic_results_always_require_human_review(self):
        decision = paper_loop.decide_with_review_loop(
            self.paper, paper_loop.HeuristicClassifier(CONFIG), CONFIG
        )

        self.assertEqual(decision.status, "needs_review")
        self.assertEqual(decision.final.source, "heuristic")
        self.assertTrue(decision.final.needs_full_text)


class SlackDigestTests(unittest.TestCase):
    def setUp(self):
        self.paper = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())[0]

    def report(self) -> dict:
        final = classification(
            section_id="5", confidence=0.73, needs_full_text=True
        )
        decision = paper_loop.LoopDecision(
            "needs_review", final, (final,), False
        )
        return {
            "run_id": "2026-08-25T233000Z",
            "generated_at": "2026-08-25T23:30:00Z",
            "classifier": "anthropic",
            "stats": {
                "discovered": 8,
                "new": 3,
                "backlog": 0,
                "prefiltered": 2,
                "queued": 1,
                "deferred": 1,
                "accepted": 0,
                "needs_review": 1,
                "rejected": 0,
            },
            "results": [
                paper_loop.result_record(
                    self.paper,
                    decision,
                    prefilter_hits=("dexterous", "tactile"),
                )
            ],
        }

    def test_payload_uses_korean_date_and_links_original_paper(self):
        payload = paper_loop.build_slack_payload(self.report(), CONFIG)
        serialized = json.dumps(payload, ensure_ascii=False)

        self.assertIn("2026-08-26", payload["text"])
        self.assertIn(self.paper.abs_url, serialized)
        self.assertIn("검토 필요", serialized)
        self.assertIn("원문 확인 필요", serialized)

    def test_missing_webhook_skips_without_exposing_secret(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                sent = paper_loop.send_slack_digest(self.report(), CONFIG)

        self.assertFalse(sent)
        self.assertIn("SLACK_WEBHOOK_URL is not configured", output.getvalue())


class PipelineTests(unittest.TestCase):
    def make_repo(self, root: Path) -> None:
        (root / "automation").mkdir(parents=True)
        (root / "content").mkdir()
        (root / "tests" / "fixtures").mkdir(parents=True)
        (root / "automation" / "paper-loop.json").write_text(
            json.dumps(CONFIG), encoding="utf-8"
        )
        (root / "automation" / "state.json").write_text(
            json.dumps({"version": 1, "papers": {}, "pending": {}}), encoding="utf-8"
        )
        (root / "automation" / "review_decisions.jsonl").write_text(
            "# human decisions\n", encoding="utf-8"
        )
        (root / "tests" / "fixtures" / "arxiv_sample.xml").write_bytes(
            FIXTURE.read_bytes()
        )
        (root / "content" / "known.md").write_text(
            "# Known Dexterous Teleoperation Paper\n\n"
            "https://arxiv.org/abs/2608.00003v2\n",
            encoding="utf-8",
        )

    def run_args(self, root: Path, *, dry_run: bool = False) -> argparse.Namespace:
        return argparse.Namespace(
            repo_root=str(root),
            config="automation/paper-loop.json",
            state="automation/state.json",
            feedback="automation/review_decisions.jsonl",
            fixture="tests/fixtures/arxiv_sample.xml",
            now="2026-08-25T00:00:00Z",
            no_llm=True,
            dry_run=dry_run,
        )

    def run_silently(self, args: argparse.Namespace) -> dict:
        with contextlib.redirect_stdout(io.StringIO()):
            return paper_loop.run_pipeline(args)

    def test_offline_run_deduplicates_writes_report_and_updates_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)

            report = self.run_silently(self.run_args(root))

            self.assertEqual(
                report["stats"],
                {
                    "discovered": 3,
                    "new": 2,
                    "backlog": 0,
                    "prefiltered": 1,
                    "queued": 1,
                    "deferred": 0,
                    "accepted": 0,
                    "needs_review": 1,
                    "rejected": 0,
                },
            )
            self.assertEqual(report["classifier"], "heuristic")
            self.assertEqual(report["results"][0]["paper"]["paper_id"], "2608.00001")
            self.assertTrue((root / "automation" / "inbox" / "latest.md").is_file())
            self.assertTrue(
                (root / "automation" / "runs" / "2026-08-25T000000Z.json").is_file()
            )
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["papers"]["2608.00001"]["status"], "needs_review")
            self.assertFalse((root / "automation" / "drafts").exists())

            repeated = self.run_silently(self.run_args(root))
            self.assertEqual(repeated["stats"]["prefiltered"], 0)
            self.assertEqual(repeated["stats"]["queued"], 0)
            self.assertEqual(repeated["results"], [])

    def test_dry_run_does_not_write_outputs_or_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            before = (root / "automation" / "state.json").read_text(encoding="utf-8")

            report = self.run_silently(self.run_args(root, dry_run=True))

            self.assertEqual(report["stats"]["needs_review"], 1)
            self.assertEqual(
                (root / "automation" / "state.json").read_text(encoding="utf-8"),
                before,
            )
            self.assertFalse((root / "automation" / "inbox").exists())

    def test_report_exposes_candidates_deferred_by_run_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            config = json.loads(
                (root / "automation" / "paper-loop.json").read_text(encoding="utf-8")
            )
            config["max_candidates_per_run"] = 1
            config["prefilter"]["include_any"].append("molecular")
            config["prefilter"]["exclude_any"] = []
            (root / "automation" / "paper-loop.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            report = self.run_silently(self.run_args(root, dry_run=True))

            self.assertEqual(report["stats"]["prefiltered"], 2)
            self.assertEqual(report["stats"]["queued"], 1)
            self.assertEqual(report["stats"]["deferred"], 1)
            self.assertEqual(len(report["results"]), 1)

    def test_deferred_candidates_persist_and_are_processed_next(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            config = json.loads(
                (root / "automation" / "paper-loop.json").read_text(encoding="utf-8")
            )
            config["max_candidates_per_run"] = 1
            config["prefilter"]["include_any"].append("molecular")
            config["prefilter"]["exclude_any"] = []
            (root / "automation" / "paper-loop.json").write_text(
                json.dumps(config), encoding="utf-8"
            )

            first = self.run_silently(self.run_args(root))
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(first["results"][0]["paper"]["paper_id"], "2608.00001")
            self.assertEqual(set(state["pending"]), {"2608.00002"})

            second = self.run_silently(self.run_args(root))
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(second["stats"]["backlog"], 1)
            self.assertEqual(second["results"][0]["paper"]["paper_id"], "2608.00002")
            self.assertEqual(state["pending"], {})

    def test_malformed_state_fails_with_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            (root / "automation" / "state.json").write_text(
                json.dumps({"version": 1, "papers": []}), encoding="utf-8"
            )

            with self.assertRaisesRegex(ValueError, "field 'papers'"):
                paper_loop.run_pipeline(self.run_args(root))


class ReviewFeedbackTests(unittest.TestCase):
    def test_accept_requires_a_configured_section(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "automation").mkdir()
            (root / "automation" / "paper-loop.json").write_text(
                json.dumps(CONFIG), encoding="utf-8"
            )
            args = argparse.Namespace(
                repo_root=str(root),
                config="automation/paper-loop.json",
                feedback="automation/review_decisions.jsonl",
                paper_id="2608.00001",
                decision="accept",
                section_id="99",
                note="invalid test",
            )

            with self.assertRaisesRegex(ValueError, "valid --section-id"):
                paper_loop.record_review(args)


if __name__ == "__main__":
    unittest.main()
