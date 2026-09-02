#!/usr/bin/env python3
"""Send one bounded failure alert without placing Slack tokens in argv or logs."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    token = os.environ.get("SLACK_BOT_TOKEN", "").strip()
    channel = os.environ.get("SLACK_CHANNEL_ID", "").strip()
    if not token or not channel:
        return 0
    detail = " ".join(sys.argv[1:]).strip() or "unknown scheduled-run failure"
    payload = json.dumps(
        {
            "channel": channel,
            "text": f":warning: Paper radar failed on Mac mini: {detail[:900]}",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://slack.com/api/chat.postMessage",
        data=payload,
        method="POST",
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json; charset=utf-8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8", "replace"))
        if not result.get("ok"):
            raise OSError(f"Slack API error: {result.get('error', 'unknown_error')}")
        return 0
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        print(f"Slack failure alert could not be sent: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
