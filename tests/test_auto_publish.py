"""Offline publication, removal, retry, and Slack ownership checks."""
import copy
import importlib
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

from scripts import paper_loop as loop
from scripts import publish_approved_paper as publisher
from tests import test_paper_loop as fixtures

CONFIG = fixtures.CONFIG


class AutoPublishTests(unittest.TestCase):
    def report(self):
        case = fixtures.SlackDigestTests()
        case.setUp()
        report = case.report()
        report["auto_publish"] = True
        report["results"][0]["decision"]["status"] = "accepted"
        return report

    def test_retry_and_every_paper_has_a_delete_button(self):
        report = self.report()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / CONFIG["output"]["runs_dir"] / (report["run_id"] + ".json")
            loop.write_json(path, report)
            with mock.patch.object(publisher, "publish", side_effect=publisher.PublishError("offline")):
                loop.retry_publications(root, CONFIG)
            self.assertEqual(loop.load_json(path, {})["results"][0]["publication"]["status"], "failed")
            with mock.patch.object(publisher, "publish", return_value={"status": "published"}) as publish:
                loop.retry_publications(root, CONFIG)
                loop.retry_publications(root, CONFIG)
                self.assertEqual(publish.call_count, 1)
            report["results"] = [copy.deepcopy(report["results"][0]) for _ in range(15)]
            for i, record in enumerate(report["results"]):
                record["paper"]["paper_id"] = f"2609.{i:05d}"
            loop.queue_slack_digest(root, report, CONFIG)
            paths = sorted((root / CONFIG["output"]["slack_outbox"]).glob("*.json"))
            ids = []
            for path in paths:
                payload = loop.load_json(path, {})["payload"]
                self.assertLessEqual(len(payload["blocks"]), 50)
                for block in payload["blocks"]:
                    if block["type"] == "actions":
                        self.assertEqual(len(block["elements"]), 1)
                        self.assertEqual(block["elements"][0]["action_id"], "paper_reject")
                        ids.append(json.loads(block["elements"][0]["value"])["paper_id"])
            self.assertEqual(len(set(ids)), 15)

    def test_uncertain_or_failed_classification_is_not_published(self):
        report = self.report()
        record = report["results"][0]
        for change in ({"retryable_error": "failed"}, {"decision": {"status": "needs_review"}}):
            with mock.patch.object(publisher, "publish") as publish:
                self.assertFalse(loop.publish_report(Path("."), {**report, "results": [{**record, **change}]}))
                publish.assert_not_called()

    def test_automatic_publication_refuses_deterministic_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            case = fixtures.PipelineTests()
            case.make_repo(root)
            args = case.run_args(root)
            args.auto_publish = args.notify_slack = True
            with mock.patch.object(publisher, "publish") as publish:
                with self.assertRaisesRegex(ValueError, "LLM provider"):
                    case.run_silently(args)
                publish.assert_not_called()

    def test_pipeline_publishes_before_notification_and_dry_run_has_no_effect(self):
        case = fixtures.PipelineTests()
        for dry_run in (True, False):
            with self.subTest(dry_run=dry_run), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                case.make_repo(root)
                args = case.run_args(root, dry_run=dry_run)
                args.auto_publish = args.notify_slack = True
                args.no_llm = False
                args.llm_provider = "anthropic"
                with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fake"}), mock.patch.object(
                    loop.AnthropicClassifier, "classify", return_value=fixtures.classification()
                ), mock.patch.object(loop, "enrich_results_with_insights"), mock.patch.object(
                    loop, "flush_slack_outbox", return_value=0
                ), mock.patch.object(publisher, "publish", return_value={"status": "published"}) as publish:
                    result = case.run_silently(args)
                if dry_run:
                    publish.assert_not_called()
                    self.assertFalse((root / CONFIG["output"]["slack_outbox"]).exists())
                else:
                    publish.assert_called_once()
                    self.assertEqual(result["results"][0]["publication"]["status"], "published")
                    path = root / CONFIG["output"]["slack_outbox"] / (result["run_id"] + ".json")
                    self.assertIn("사이트 자동 반영 완료", json.dumps(loop.load_json(path, {}), ensure_ascii=False))

    def test_slack_removal_requires_owner_and_preserves_retry_button_on_failure(self):
        handlers = {}

        class FakeApp:
            def __init__(self, **kwargs):
                pass

            def action(self, name):
                def register(handler):
                    handlers[name] = handler
                    return handler
                return register

        modules = {
            "slack_bolt": types.SimpleNamespace(App=FakeApp),
            "slack_bolt.adapter": types.ModuleType("slack_bolt.adapter"),
            "slack_bolt.adapter.socket_mode": types.SimpleNamespace(SocketModeHandler=mock.Mock()),
        }
        with mock.patch.dict(sys.modules, modules), mock.patch.dict(os.environ, {
            "SLACK_BOT_TOKEN": "fake", "SLACK_APPROVER_USER_ID": "owner"
        }):
            bot = importlib.import_module("scripts.slack_review_bot")
            bot.build_app(Path("."))
            body = {"user": {"id": "stranger"}, "actions": [{"value": json.dumps({
                "run_id": "run", "paper_id": "2609.00001", "section_id": "7"
            })}]}
            ack, respond, client = mock.Mock(), mock.Mock(), mock.Mock()
            with mock.patch.object(bot, "publish", side_effect=publisher.PublishError("busy")) as publish:
                handlers["paper_reject"](ack, body, client, respond)
                publish.assert_not_called()
                ack.assert_called_once()
                body["user"]["id"] = "owner"
                handlers["paper_reject"](ack, body, client, respond)
                self.assertTrue(publish.call_args.kwargs["reject"])
                self.assertIn("재시도", respond.call_args.kwargs["text"])
                client.chat_update.assert_not_called()

    def test_real_git_publish_remove_and_prevent_republication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "checkout"
            remote = Path(directory) / "remote.git"
            root.mkdir()
            remote.mkdir()
            git = publisher.run
            git(("git", "init", "--bare"), cwd=remote)
            git(("git", "init", "-b", "main"), cwd=root)
            git(("git", "config", "user.email", "test@example.invalid"), cwd=root)
            git(("git", "config", "user.name", "Offline test"), cwd=root)
            git(("git", "remote", "add", "origin", str(remote)), cwd=root)
            (root / "content").mkdir()
            (root / "docs").mkdir()
            (root / "tests").mkdir()
            (root / ".gitignore").write_text("__pycache__/\n*.pyc\n", encoding="utf-8")
            (root / "tests/test_smoke.py").write_text(
                "import unittest\nclass Smoke(unittest.TestCase):\n    def test_ok(self): self.assertTrue(True)\n",
                encoding="utf-8",
            )
            shutil.copyfile(Path(__file__).resolve().parents[1] / "build.py", root / "build.py")
            original = "## 7. Papers\n| Paper | Year |\n|---|---|\n| Existing | 2025 |\n"
            for name in publisher.SURVEYS:
                (root / "content" / name).write_text(original, encoding="utf-8")
            report = self.report()
            paper_id = report["results"][0]["paper"]["paper_id"]
            loop.write_json(root / "automation/paper-loop.json", CONFIG)
            loop.write_json(root / "automation/runs" / (report["run_id"] + ".json"), report)
            git(("git", "add", "."), cwd=root)
            git(("git", "commit", "-m", "Initial test site"), cwd=root)
            git(("git", "push", "origin", "main"), cwd=root)
            commands = []

            def fake_agent(command, *, cwd, **kwargs):
                commands.append(tuple(command))
                if len(command) > 1 and command[1] == "exec":
                    for name in publisher.SURVEYS:
                        path = cwd / "content" / name
                        path.write_text(path.read_text(encoding="utf-8") +
                                        f"| [New](https://arxiv.org/abs/{paper_id}) | 2026 |\n", encoding="utf-8")
                    for folder in ("detailed", "detailed_ko", "detailed_zh"):
                        path = cwd / "content" / folder / "section7/new.md"
                        path.parent.mkdir(parents=True)
                        path.write_text(f"# New\nhttps://arxiv.org/abs/{paper_id}\n", encoding="utf-8")
                    return ""
                return git(command, cwd=cwd, **kwargs)

            args = dict(repo_root=root, run_id=report["run_id"], paper_id=paper_id,
                        section_id="7", dry_run=False)
            with mock.patch.object(publisher, "run", side_effect=fake_agent), mock.patch.object(
                publisher.shutil, "which", return_value="codex"
            ), mock.patch.object(publisher, "fetch_analysis_source", return_value=("arxiv_html", "url", "[L0001] source")):
                self.assertEqual(publisher.publish(**args)["status"], "published")
                # Add unrelated content remotely after publication. Removal must preserve it.
                git(("git", "pull", "--ff-only", "origin", "main"), cwd=root)
                self.assertEqual(len(list((root / "docs").rglob("new.html"))), 3)
                for name in publisher.SURVEYS:
                    path = root / "content" / name
                    path.write_text(path.read_text(encoding="utf-8") + "| Another paper | 2026 |\n", encoding="utf-8")
                git(("git", "add", "content"), cwd=root)
                git(("git", "commit", "-m", "Another paper"), cwd=root)
                git(("git", "push", "origin", "main"), cwd=root)
                self.assertEqual(publisher.publish(**args, reject=True)["status"], "rejected")
                self.assertEqual(publisher.publish(**args, reject=True)["status"], "rejected")
                (root / "automation/review_decisions.jsonl").unlink()
                # Even a lost local feedback file cannot undo the remote tombstone.
                self.assertEqual(publisher.publish(**args)["status"], "rejected")
            self.assertEqual(sum(len(c) > 1 and c[1] == "exec" for c in commands), 1)
            git(("git", "pull", "--ff-only", "origin", "main"), cwd=root)
            for name in publisher.SURVEYS:
                self.assertEqual((root / "content" / name).read_text(encoding="utf-8"), original + "| Another paper | 2026 |\n")
            self.assertFalse(list((root / "content").glob("detailed*/section7/new.md")))
            self.assertFalse(list((root / "docs").rglob("new.html")))
            self.assertEqual(loop.load_json(root / f"automation/publications/{paper_id}.json", {})["status"], "rejected")

    def test_changed_content_blocks_removal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "content").mkdir()
            paper_id = "2609.00001"
            row = f"| [Paper](https://arxiv.org/abs/{paper_id}) | 2026 |"
            for name in publisher.SURVEYS:
                (root / "content" / name).write_text(row + "\n", encoding="utf-8")
            manifest = {"paper_id": paper_id, "rows": {name: row for name in publisher.SURVEYS}, "details": {}}
            (root / "content/survey_ko.md").write_text(row.replace("Paper", "Edited"), encoding="utf-8")
            before = publisher.content_snapshot(root)
            with self.assertRaises(publisher.PublishError):
                publisher.remove_publication(root, manifest, paper_id)
            self.assertEqual(before, publisher.content_snapshot(root))


if __name__ == "__main__":
    unittest.main()
