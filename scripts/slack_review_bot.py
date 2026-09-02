#!/usr/bin/env python3
"""Receive owner-only Slack approvals over Socket Mode."""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

try:
    from .paper_loop import load_json, record_review_decision
    from .publish_approved_paper import PublishError, publish
except ImportError:
    from paper_loop import load_json, record_review_decision
    from publish_approved_paper import PublishError, publish


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLISH_LOCK = threading.Lock()


def action_value(body: dict[str, Any]) -> dict[str, str]:
    actions = body.get("actions", [])
    if len(actions) != 1:
        raise ValueError("Expected exactly one Slack action")
    value = json.loads(actions[0].get("value", ""))
    required = ("run_id", "paper_id", "section_id")
    if not isinstance(value, dict) or any(not str(value.get(key, "")) for key in required):
        raise ValueError("Invalid Slack action value")
    return {key: str(value[key]) for key in required}


def status_blocks(
    body: dict[str, Any], text: str, *, keep_actions: bool = False
) -> list[dict[str, Any]]:
    action = body["actions"][0]
    target = action.get("block_id")
    updated: list[dict[str, Any]] = []
    for block in body.get("message", {}).get("blocks", []):
        if block.get("block_id") != target:
            updated.append(block)
            continue
        updated.append(
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": text}],
            }
        )
        if keep_actions:
            updated.append(block)
    return updated


def update_message(client: Any, body: dict[str, Any], blocks: list[dict[str, Any]]) -> None:
    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        text=body["message"].get("text", "Paper radar review"),
        blocks=blocks,
    )


def authorized(body: dict[str, Any]) -> bool:
    return body.get("user", {}).get("id") == os.environ.get(
        "SLACK_APPROVER_USER_ID", ""
    )


def build_app(repo_root: Path = REPO_ROOT) -> App:
    app = App(token=os.environ["SLACK_BOT_TOKEN"])
    config_path = repo_root / "automation" / "paper-loop.json"

    @app.action("paper_reject")
    def reject(ack: Any, body: dict[str, Any], client: Any, respond: Any) -> None:
        ack()
        if not authorized(body):
            respond(text="이 작업을 승인할 권한이 없습니다.", response_type="ephemeral")
            return
        try:
            value = action_value(body)
            config = load_json(config_path, None)
            if not isinstance(config, dict):
                raise ValueError("Invalid paper-radar config")
            record_review_decision(
                feedback_path=repo_root / "automation" / "review_decisions.jsonl",
                config=config,
                paper_id=value["paper_id"],
                decision="reject",
                section_id="0",
                note=f"Rejected in Slack by {body['user']['id']}",
            )
            update_message(
                client,
                body,
                status_blocks(body, f"❌ `{value['paper_id']}` 제외됨"),
            )
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            respond(text=f"제외 기록 실패: {error}", response_type="ephemeral")

    @app.action("paper_approve")
    def approve(ack: Any, body: dict[str, Any], client: Any, respond: Any) -> None:
        ack()
        if not authorized(body):
            respond(text="이 작업을 승인할 권한이 없습니다.", response_type="ephemeral")
            return
        try:
            value = action_value(body)
        except (ValueError, KeyError, json.JSONDecodeError) as error:
            respond(text=f"승인 정보 오류: {error}", response_type="ephemeral")
            return
        if not PUBLISH_LOCK.acquire(blocking=False):
            respond(text="다른 논문을 반영 중입니다. 잠시 후 다시 눌러주세요.", response_type="ephemeral")
            return
        try:
            update_message(
                client,
                body,
                status_blocks(body, f"⏳ `{value['paper_id']}` 원문 확인·빌드 중"),
            )
            result = publish(
                repo_root=repo_root,
                run_id=value["run_id"],
                paper_id=value["paper_id"],
                section_id=value["section_id"],
                dry_run=False,
            )
            status = result["status"]
            commit = str(result.get("commit", ""))[:12]
            label = "이미 반영됨" if status == "already_published" else f"반영 완료 `{commit}`"
            update_message(
                client,
                body,
                status_blocks(body, f"✅ `{value['paper_id']}` {label}"),
            )
        except (OSError, ValueError, KeyError, PublishError) as error:
            update_message(
                client,
                body,
                status_blocks(
                    body,
                    f"⚠️ `{value['paper_id']}` 반영 실패: {str(error)[:240]}",
                    keep_actions=True,
                ),
            )
        finally:
            PUBLISH_LOCK.release()

    return app


def main() -> int:
    required = ("SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_APPROVER_USER_ID")
    missing = [name for name in required if not os.environ.get(name, "").strip()]
    if missing:
        raise SystemExit(f"Missing environment variable(s): {', '.join(missing)}")
    SocketModeHandler(build_app(), os.environ["SLACK_APP_TOKEN"]).start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
