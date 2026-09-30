#!/usr/bin/env python3
"""Receive owner-only paper rejections over Slack Socket Mode."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

try:
    from .publish_approved_paper import publish
except ImportError:
    from publish_approved_paper import publish


REPO_ROOT = Path(__file__).resolve().parents[1]


def action_value(body: dict[str, Any]) -> dict[str, str]:
    actions = body.get("actions", [])
    if len(actions) != 1:
        raise ValueError("Expected exactly one Slack action")
    value = json.loads(actions[0].get("value", ""))
    required = ("run_id", "paper_id", "section_id")
    if not isinstance(value, dict) or any(not str(value.get(key, "")) for key in required):
        raise ValueError("Invalid Slack action value")
    return {key: str(value[key]) for key in required}


def authorized(body: dict[str, Any]) -> bool:
    return body.get("user", {}).get("id") == os.environ.get(
        "SLACK_APPROVER_USER_ID", ""
    )


def build_app(repo_root: Path = REPO_ROOT) -> App:
    app = App(token=os.environ["SLACK_BOT_TOKEN"])

    @app.action("paper_reject")
    def reject(ack: Any, body: dict[str, Any], client: Any, respond: Any) -> None:
        ack()
        if not authorized(body):
            respond(text="이 작업을 수행할 권한이 없습니다.", response_type="ephemeral")
            return
        try:
            value = action_value(body)
            respond(text="사이트 삭제와 재등록 방지를 처리 중입니다.", response_type="ephemeral")
            publish(repo_root=repo_root, run_id=value["run_id"], paper_id=value["paper_id"],
                    section_id=value["section_id"], dry_run=False, reject=True)
            # Keep the original digest intact: simultaneous clicks on different
            # papers must not overwrite each other's message state.
            respond(text=f"❌ `{value['paper_id']}` 삭제 반영 완료 · 다시 등록하지 않습니다. "
                         "사이트 배포가 완료되면 삭제가 표시됩니다.", response_type="ephemeral")
        except (OSError, ValueError, KeyError, RuntimeError) as error:
            respond(text=f"삭제 실패: {str(error)[:240]} · 잠시 후 같은 버튼으로 재시도하세요.",
                    response_type="ephemeral")

    @app.action("paper_approve")
    def old_approve(ack: Any, respond: Any) -> None:
        ack()
        respond(text="수동 승인 기능은 종료되었습니다. 검증된 후보는 정기 실행에서 자동 반영됩니다.",
                response_type="ephemeral")

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
