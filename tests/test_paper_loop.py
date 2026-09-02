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
from scripts import publish_approved_paper


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

    def test_arxiv_pagination_advances_start_and_stops_on_short_page(self):
        config = json.loads(json.dumps(CONFIG))
        config["queries"] = [{"name": "test", "search_query": "cat:cs.RO"}]
        config["source"]["max_results_per_query"] = 3
        config["source"]["max_pages_per_query"] = 4
        config["source"]["request_delay_seconds"] = 0
        empty = (
            b'<?xml version="1.0" encoding="UTF-8"?>'
            b'<feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        )
        urls: list[str] = []

        def fake_request(url, **kwargs):
            del kwargs
            urls.append(url)
            return FIXTURE.read_bytes() if len(urls) == 1 else empty

        with mock.patch("scripts.paper_loop.request_bytes", side_effect=fake_request):
            papers = paper_loop.fetch_arxiv(config)

        self.assertEqual(len(papers), 3)
        self.assertEqual(len(urls), 2)
        self.assertIn("start=0", urls[0])
        self.assertIn("start=3", urls[1])

    def test_one_timed_out_query_does_not_abort_the_remaining_queries(self):
        config = json.loads(json.dumps(CONFIG))
        config["queries"] = [
            {"name": "offline", "search_query": "cat:cs.RO"},
            {"name": "working", "search_query": "cat:cs.AI"},
        ]
        config["source"]["max_pages_per_query"] = 1
        config["source"]["request_delay_seconds"] = 0

        with mock.patch(
            "scripts.paper_loop.request_bytes",
            side_effect=(RuntimeError("timeout"), FIXTURE.read_bytes()),
        ):
            with contextlib.redirect_stderr(io.StringIO()) as output:
                papers = paper_loop.fetch_arxiv(config)

        self.assertEqual(len(papers), 3)
        self.assertIn("offline", output.getvalue())

    def test_all_timed_out_queries_still_fail_closed(self):
        config = json.loads(json.dumps(CONFIG))
        config["queries"] = [{"name": "offline", "search_query": "cat:cs.RO"}]
        config["source"]["max_pages_per_query"] = 1
        config["source"]["request_delay_seconds"] = 0

        with mock.patch(
            "scripts.paper_loop.request_bytes", side_effect=RuntimeError("timeout")
        ):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, "All arXiv queries failed"):
                    paper_loop.fetch_arxiv(config)

    def test_arxiv_overlapping_queries_merge_provenance(self):
        config = json.loads(json.dumps(CONFIG))
        config["queries"] = [
            {"name": "control", "search_query": "cat:eess.SY"},
            {"name": "robotics", "search_query": "cat:cs.RO"},
        ]
        config["source"]["max_results_per_query"] = 10
        config["source"]["max_pages_per_query"] = 2
        config["source"]["request_delay_seconds"] = 0

        with mock.patch(
            "scripts.paper_loop.request_bytes", return_value=FIXTURE.read_bytes()
        ) as request:
            papers = paper_loop.fetch_arxiv(config)

        self.assertEqual(request.call_count, 2)
        self.assertEqual(len(papers), 3)
        self.assertEqual(papers[0].query_names, ("control", "robotics"))

    def test_overlapping_full_pages_are_bounded_and_merge_query_names(self):
        config = json.loads(json.dumps(CONFIG))
        config["queries"] = [
            {"name": "first", "search_query": "cat:cs.RO"},
            {"name": "second", "search_query": "cat:cs.AI"},
        ]
        config["source"]["max_results_per_query"] = 3
        config["source"]["max_pages_per_query"] = 2
        config["source"]["request_delay_seconds"] = 0
        urls: list[str] = []

        def repeated_page(url, **kwargs):
            del kwargs
            urls.append(url)
            return FIXTURE.read_bytes()

        with mock.patch("scripts.paper_loop.request_bytes", side_effect=repeated_page):
            papers = paper_loop.fetch_arxiv(config)

        self.assertEqual(len(urls), 4)
        self.assertEqual(len(papers), 3)
        self.assertEqual(papers[0].query_names, ("first", "second"))


class ScreeningTests(unittest.TestCase):
    def test_priority_ranking_is_not_input_order(self):
        papers = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())
        ordinary = dataclasses.replace(
            papers[0], paper_id="ordinary", title="Robot hand design", summary="hardware"
        )
        priority = dataclasses.replace(
            papers[0],
            paper_id="priority",
            title="Sim-to-real reinforcement learning for quadruped locomotion",
            summary="Domain randomization and PPO for a legged robot.",
            query_names=("legged-humanoid",),
        )
        now = paper_loop.parse_iso_datetime("2026-08-25T00:00:00Z")
        candidates = [
            paper_loop.Candidate(ordinary, ("robot hand",), "2026-08-25T00:00:00Z"),
            paper_loop.Candidate(
                priority, ("reinforcement learning", "quadruped"), "2026-08-25T00:00:00Z"
            ),
        ]

        ranked = paper_loop.rank_candidates(candidates, CONFIG, now=now)

        self.assertEqual(ranked[0][0].paper.paper_id, "priority")
        self.assertIn("physical-ai-robot-learning", ranked[0][1].matched_topics)

    def test_oldest_backlog_gets_reserved_capacity(self):
        papers = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())
        ranked = [
            (
                paper_loop.Candidate(
                    dataclasses.replace(papers[0], paper_id=f"fresh-{index}"),
                    ("robot hand",),
                    "2026-08-25T00:00:00Z",
                    False,
                ),
                paper_loop.ScreeningResult(100 - index, (), ()),
            )
            for index in range(3)
        ]
        oldest = (
            paper_loop.Candidate(
                dataclasses.replace(papers[0], paper_id="oldest"),
                ("robot hand",),
                "2026-07-01T00:00:00Z",
                True,
            ),
            paper_loop.ScreeningResult(1, (), ()),
        )

        selected = paper_loop.select_with_backlog_reserve(
            [*ranked, oldest], limit=2, reserve_fraction=0.5
        )

        self.assertIn("oldest", {item[0].paper.paper_id for item in selected})

    def test_priority_ties_use_stable_paper_id_order(self):
        base = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())[0]
        records = []
        for paper_id in ("b", "a"):
            current = dataclasses.replace(base, paper_id=paper_id)
            decision = paper_loop.LoopDecision(
                "needs_review",
                classification(source="test"),
                (classification(source="test"),),
                False,
            )
            records.append(
                paper_loop.result_record(
                    current,
                    decision,
                    prefilter_hits=("robot hand",),
                    screening=paper_loop.ScreeningResult(10.0, (), ()),
                )
            )

        ordered = paper_loop.prioritized_results(records)

        self.assertEqual([item["paper"]["paper_id"] for item in ordered], ["a", "b"])

    def test_expanded_topics_survive_prefilter_and_map_to_taxonomy(self):
        cases = [
            ("Quadruped whole-body control", "Legged robot locomotion", "13"),
            ("Learning-based model predictive control", "Safe control", "14"),
            ("Bimanual robot manipulation", "Diffusion policy", "15"),
            ("Motion planning", "Task planning and trajectory optimization", "16"),
            ("Visual-inertial state estimation", "Sensor fusion", "17"),
            ("Physical AI", "Robot world model and embodied foundation model", "18"),
        ]
        for index, (title, summary, section_id) in enumerate(cases):
            with self.subTest(section_id=section_id):
                paper = paper_loop.Paper(
                    paper_id=f"topic-{index}",
                    title=title,
                    summary=summary,
                    authors=(),
                    published="2026-08-25T00:00:00Z",
                    updated="2026-08-25T00:00:00Z",
                    categories=("cs.RO",),
                    abs_url=f"https://arxiv.org/abs/topic-{index}",
                    pdf_url="",
                )
                keep, _ = paper_loop.prefilter(paper, CONFIG)
                result = paper_loop.HeuristicClassifier(CONFIG).classify(
                    paper, mode="initial"
                )
                self.assertTrue(keep)
                self.assertEqual(result.section_id, section_id)

        excluded = dataclasses.replace(
            paper,
            paper_id="excluded",
            title="Safe control for financial market trading",
        )
        self.assertFalse(paper_loop.prefilter(excluded, CONFIG)[0])

    def test_equal_priority_results_have_stable_paper_id_tie_break(self):
        paper = paper_loop.parse_arxiv_atom(FIXTURE.read_bytes())[0]
        final = classification(confidence=0.8)
        decision = paper_loop.LoopDecision("needs_review", final, (final,), False)
        records = [
            paper_loop.result_record(
                dataclasses.replace(paper, paper_id=paper_id),
                decision,
                prefilter_hits=("tactile",),
                screening=paper_loop.ScreeningResult(5.0, (), ()),
            )
            for paper_id in ("z-paper", "a-paper", "m-paper")
        ]

        ordered = paper_loop.prioritized_results(records)

        self.assertEqual(
            [item["paper"]["paper_id"] for item in ordered],
            ["a-paper", "m-paper", "z-paper"],
        )


class LockTests(unittest.TestCase):
    def test_dead_pid_lock_is_reclaimed_but_live_lock_is_not(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / ".state.lock"
            lock.write_text(
                json.dumps({"pid": 99999999, "started_at": "2026-08-25T00:00:00Z"}),
                encoding="utf-8",
            )
            with mock.patch("scripts.paper_loop.utc_now", return_value=paper_loop.parse_iso_datetime("2026-08-25T00:01:00Z")):
                with paper_loop.exclusive_run_lock(lock):
                    self.assertTrue(lock.exists())
            self.assertFalse(lock.exists())

            lock.write_text(
                json.dumps({"pid": paper_loop.os.getpid(), "started_at": "2020-01-01T00:00:00Z"}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "Another paper-loop run"):
                with paper_loop.exclusive_run_lock(lock):
                    pass
            self.assertTrue(lock.exists())

    def test_old_empty_lock_from_crash_is_reclaimed(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / ".state.lock"
            lock.write_text("", encoding="utf-8")
            old = paper_loop.parse_iso_datetime("2026-08-24T00:00:00Z").timestamp()
            paper_loop.os.utime(lock, (old, old))

            with mock.patch(
                "scripts.paper_loop.utc_now",
                return_value=paper_loop.parse_iso_datetime("2026-08-25T00:00:00Z"),
            ):
                with paper_loop.exclusive_run_lock(lock):
                    self.assertTrue(lock.exists())

            self.assertFalse(lock.exists())

    def test_recent_malformed_lock_still_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / ".state.lock"
            lock.write_text("{incomplete", encoding="utf-8")
            recent = paper_loop.parse_iso_datetime("2026-08-25T00:00:00Z").timestamp()
            paper_loop.os.utime(lock, (recent, recent))

            with mock.patch(
                "scripts.paper_loop.utc_now",
                return_value=paper_loop.parse_iso_datetime("2026-08-25T00:01:00Z"),
            ):
                with self.assertRaisesRegex(RuntimeError, "Another paper-loop run"):
                    with paper_loop.exclusive_run_lock(lock):
                        pass

            self.assertTrue(lock.exists())


class AtomicWriteTests(unittest.TestCase):
    def test_failed_replace_preserves_previous_state_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text('{"old": true}\n', encoding="utf-8")

            with mock.patch("scripts.paper_loop.os.replace", side_effect=OSError("disk")):
                with self.assertRaisesRegex(OSError, "disk"):
                    paper_loop.write_json(path, {"new": True})

            self.assertEqual(path.read_text(encoding="utf-8"), '{"old": true}\n')
            self.assertEqual(list(path.parent.glob(".state.json.*.tmp")), [])


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


class FullTextInsightTests(unittest.TestCase):
    def test_html_extraction_removes_scripts_and_numbers_source_lines(self):
        payload = b"""
        <html><body><h1>Method</h1><p>Contact-rich policy.</p>
        <script>ignore_me()</script><table><tr><td>Success</td><td>82%</td></tr></table>
        </body></html>
        """

        text = paper_loop.extract_arxiv_html_text(payload)
        numbered = paper_loop.number_source_lines(text, max_chars=1000)

        self.assertNotIn("ignore_me", text)
        self.assertIn("[L0001] Method", numbered)
        self.assertIn("82%", numbered)

    def test_validation_recomputes_only_same_condition_delta(self):
        base = {
            "problem": "접촉 작업의 성공률 저하",
            "method": "촉각 기반 정책",
            "contribution": "동일 benchmark에서 성공률 향상",
            "limitations": ["단일 로봇에서만 평가 [L0040]"],
            "gap_candidate": "다른 embodiment 검증 필요",
            "evidence": ["[L0010] 문제와 방법", "[L0030] 결과 표"],
            "comparisons": [
                {
                    "task": "insertion",
                    "dataset": "Benchmark A",
                    "metric": "success rate",
                    "proposed_value": 82,
                    "baseline_name": "Baseline X",
                    "baseline_value": 70,
                    "unit": "%",
                    "higher_is_better": True,
                    "conditions_match": True,
                    "comparison_note": "동일 조건",
                    "proposed_evidence": "[L0030] proposed 82%",
                    "baseline_evidence": "[L0030] baseline 70%",
                },
                {
                    "task": "insertion",
                    "dataset": "Benchmark B",
                    "metric": "success rate",
                    "proposed_value": 90,
                    "baseline_name": "Baseline Y",
                    "baseline_value": 60,
                    "unit": "%",
                    "higher_is_better": True,
                    "conditions_match": False,
                    "comparison_note": "평가 물체 수가 다름",
                    "proposed_evidence": "[L0031] proposed 90%",
                    "baseline_evidence": "[L0032] baseline 60%",
                },
            ],
        }

        insight = paper_loop.validate_insight(
            base, source_kind="arxiv_html", source_url="https://arxiv.org/html/test"
        )

        matched, mismatched = insight["comparisons"]
        self.assertEqual(matched["absolute_delta"], 12)
        self.assertAlmostEqual(matched["relative_improvement_percent"], 1200 / 70)
        self.assertIsNone(mismatched["absolute_delta"])
        self.assertIsNone(mismatched["relative_improvement_percent"])


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
        self.assertIn("paper_approve", serialized)
        self.assertIn("paper_reject", serialized)

    def test_missing_bot_configuration_skips_without_exposing_secret(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                sent = paper_loop.send_slack_digest(self.report(), CONFIG)

        self.assertFalse(sent)
        self.assertIn("SLACK_BOT_TOKEN or SLACK_CHANNEL_ID", output.getvalue())

    def test_payload_prefers_grounded_insight_over_abstract_summary(self):
        report = self.report()
        report["results"][0]["insight"] = {
            "problem": "접촉 상태 변화에서 성공률이 낮아지는 문제",
            "method": "촉각 기반 variable impedance policy",
            "contribution": "동일 조건 baseline보다 성공률을 높임",
            "limitations": ["단일 task 평가"],
            "gap_candidate": "다른 hand로의 일반화 검증",
            "comparisons": [],
            "evidence": ["[L0010] task and result"],
            "source_kind": "arxiv_html",
            "source_url": "https://arxiv.org/html/2608.00001v1",
        }

        payload = paper_loop.build_slack_payload(report, CONFIG)
        serialized = json.dumps(payload, ensure_ascii=False)

        self.assertIn("*문제*", serialized)
        self.assertIn("*Gap 후보*", serialized)
        self.assertIn("직접 비교 가능한 동일 조건 수치 없음", serialized)

    def test_configured_bot_posts_block_kit_payload(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                del args

            @staticmethod
            def read():
                return b'{"ok": true}'

        with mock.patch.dict(
            "os.environ",
            {"SLACK_BOT_TOKEN": "xoxb-secret", "SLACK_CHANNEL_ID": "C123"},
        ):
            with mock.patch(
                "scripts.paper_loop.urllib.request.urlopen",
                return_value=FakeResponse(),
            ) as urlopen:
                with contextlib.redirect_stdout(io.StringIO()):
                    sent = paper_loop.send_slack_digest(self.report(), CONFIG)

        self.assertTrue(sent)
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(request.full_url, "https://slack.com/api/chat.postMessage")
        self.assertEqual(payload["channel"], "C123")
        self.assertIn("blocks", payload)

    def test_failed_slack_payload_remains_in_durable_outbox(self):
        config = json.loads(json.dumps(CONFIG))
        config["slack"]["request_attempts"] = 1
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = paper_loop.queue_slack_digest(root, self.report(), config)
            with mock.patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-secret", "SLACK_CHANNEL_ID": "C123"},
            ):
                with mock.patch(
                    "scripts.paper_loop.urllib.request.urlopen",
                    side_effect=TimeoutError("offline"),
                ):
                    with contextlib.redirect_stderr(io.StringIO()):
                        sent = paper_loop.flush_slack_outbox(root, config)

            self.assertEqual(sent, 0)
            self.assertTrue(path.exists())

    def test_successful_outbox_replay_is_not_sent_twice(self):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                del args

            @staticmethod
            def read():
                return b'{"ok": true}'

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = paper_loop.queue_slack_digest(root, self.report(), CONFIG)
            with mock.patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-secret", "SLACK_CHANNEL_ID": "C123"},
            ):
                with mock.patch(
                    "scripts.paper_loop.urllib.request.urlopen",
                    return_value=FakeResponse(),
                ) as urlopen:
                    self.assertEqual(paper_loop.flush_slack_outbox(root, CONFIG), 1)
                    self.assertEqual(paper_loop.flush_slack_outbox(root, CONFIG), 0)

            self.assertFalse(path.exists())
            self.assertEqual(urlopen.call_count, 1)


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
                    "retained_filtered_backlog": 0,
                    "prefiltered": 1,
                    "screened": 1,
                    "screening_deferred": 0,
                    "queued": 1,
                    "deep_analysis_selected": 1,
                    "deep_analysis_deferred": 0,
                    "deferred": 0,
                    "retryable_failures": 0,
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
            self.assertEqual(repeated["stats"]["new"], 0)
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

    def test_pending_survives_a_later_prefilter_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            config_path = root / "automation" / "paper-loop.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["max_candidates_per_run"] = 1
            config["prefilter"]["include_any"].append("molecular")
            config["prefilter"]["exclude_any"] = []
            config_path.write_text(json.dumps(config), encoding="utf-8")

            self.run_silently(self.run_args(root))
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )
            self.assertIn("2608.00002", state["pending"])

            config["prefilter"]["exclude_any"] = ["molecular"]
            config_path.write_text(json.dumps(config), encoding="utf-8")
            second = self.run_silently(self.run_args(root))
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )

            self.assertEqual(second["stats"]["retained_filtered_backlog"], 1)
            self.assertEqual(
                state["pending"]["2608.00002"]["deferred_reason"],
                "current_prefilter_no_match",
            )

    def test_outside_lookback_papers_are_seen_only_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            args = self.run_args(root)
            args.now = "2027-08-25T00:00:00Z"

            first = self.run_silently(args)
            second = self.run_silently(args)

            self.assertEqual(first["stats"]["new"], 2)
            self.assertEqual(first["results"], [])
            self.assertEqual(second["stats"]["new"], 0)

    def test_retryable_codex_failure_is_processed_on_next_run(self):
        from scripts.codex_batch_classifier import CodexExecutionError

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            args = self.run_args(root)
            args.no_llm = False
            args.llm_provider = "codex"

            with mock.patch(
                "scripts.paper_loop.decide_codex_batch",
                side_effect=CodexExecutionError("temporary login failure"),
            ):
                first = self.run_silently(args)
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(first["stats"]["retryable_failures"], 1)
            self.assertIn("2608.00001", state["pending"])
            self.assertNotIn("2608.00001", state["papers"])

            def successful_batch(papers, config, *, repo_root):
                del config, repo_root
                final = classification(source="codex_cli_review")
                return {
                    paper.paper_id: paper_loop.LoopDecision(
                        "needs_review", final, (final,), False
                    )
                    for paper in papers
                }

            with mock.patch(
                "scripts.paper_loop.decide_codex_batch", side_effect=successful_batch
            ), mock.patch("scripts.paper_loop.enrich_results_with_codex_insights"):
                second = self.run_silently(args)
            state = json.loads(
                (root / "automation" / "state.json").read_text(encoding="utf-8")
            )

            self.assertEqual(second["stats"]["retryable_failures"], 0)
            self.assertIn("2608.00001", state["papers"])
            self.assertNotIn("2608.00001", state["pending"])

    def test_slack_payload_is_queued_before_processed_state_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            args = self.run_args(root)
            args.notify_slack = True
            events: list[str] = []
            original_write_json = paper_loop.write_json

            def tracked_write(path, value):
                if Path(path).resolve() == (root / "automation" / "state.json").resolve():
                    events.append("state")
                return original_write_json(path, value)

            def tracked_queue(*args, **kwargs):
                del args, kwargs
                events.append("queue")
                return root / "queued.json"

            with mock.patch("scripts.paper_loop.write_json", side_effect=tracked_write), mock.patch(
                "scripts.paper_loop.queue_slack_digest", side_effect=tracked_queue
            ), mock.patch("scripts.paper_loop.flush_slack_outbox", return_value=0):
                self.run_silently(args)

            self.assertLess(events.index("queue"), events.index("state"))

    def test_slack_queue_failure_does_not_commit_processed_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            args = self.run_args(root)
            args.notify_slack = True
            state_path = root / "automation" / "state.json"
            before = state_path.read_text(encoding="utf-8")

            with mock.patch(
                "scripts.paper_loop.queue_slack_digest",
                side_effect=OSError("outbox disk failure"),
            ), mock.patch("scripts.paper_loop.flush_slack_outbox", return_value=0):
                with self.assertRaisesRegex(OSError, "outbox disk failure"):
                    self.run_silently(args)

            self.assertEqual(state_path.read_text(encoding="utf-8"), before)

    def test_run_without_notify_does_not_flush_existing_outbox(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            args = self.run_args(root)
            args.notify_slack = False

            with mock.patch("scripts.paper_loop.flush_slack_outbox") as flush:
                self.run_silently(args)

            flush.assert_not_called()

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

    def test_identical_slack_click_is_recorded_once(self):
        with tempfile.TemporaryDirectory() as directory:
            feedback = Path(directory) / "review.jsonl"
            first, first_added = paper_loop.record_review_decision(
                feedback_path=feedback,
                config=CONFIG,
                paper_id="2608.00001",
                decision="reject",
                section_id="0",
            )
            second, second_added = paper_loop.record_review_decision(
                feedback_path=feedback,
                config=CONFIG,
                paper_id="2608.00001",
                decision="reject",
                section_id="0",
            )

            self.assertTrue(first_added)
            self.assertFalse(second_added)
            self.assertEqual(first, second)
            self.assertEqual(len(paper_loop.load_feedback(feedback)), 1)


class ApprovedPublishTests(unittest.TestCase):
    def test_publisher_rejects_changes_outside_content_and_docs(self):
        publish_approved_paper.require_allowed_changes(
            {"content/survey.md", "docs/index.html"}, ("content/", "docs/")
        )
        with self.assertRaisesRegex(publish_approved_paper.PublishError, "Unexpected"):
            publish_approved_paper.require_allowed_changes(
                {"content/survey.md", "scripts/paper_loop.py"},
                ("content/", "docs/"),
            )


if __name__ == "__main__":
    unittest.main()
