#!/usr/bin/env python3
"""Send one bounded failure alert without placing the webhook in argv or logs."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    webhook = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not webhook:
        return 0
    detail = " ".join(sys.argv[1:]).strip() or "unknown scheduled-run failure"
    payload = json.dumps(
        {"text": f":warning: Paper radar failed on Mac mini: {detail[:900]}"}
    ).encode("utf-8")
    request = urllib.request.Request(
        webhook,
        data=payload,
        method="POST",
        headers={"content-type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response.read()
        return 0
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"Slack failure alert could not be sent: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
