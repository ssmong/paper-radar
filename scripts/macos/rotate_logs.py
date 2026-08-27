#!/usr/bin/env python3
"""Bound the two LaunchAgent logs without touching any other path."""

from __future__ import annotations

import sys
from pathlib import Path


MAX_BYTES = 2 * 1024 * 1024


def rotate(path: Path) -> None:
    if not path.is_file() or path.stat().st_size <= MAX_BYTES:
        return
    oldest = path.with_name(path.name + ".2")
    previous = path.with_name(path.name + ".1")
    if oldest.exists():
        oldest.unlink()
    if previous.exists():
        previous.replace(oldest)
    path.replace(previous)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: rotate_logs.py /absolute/log/directory", file=sys.stderr)
        return 64
    root = Path(sys.argv[1])
    if not root.is_absolute() or root.name != "paper-radar":
        print("refusing unexpected log directory", file=sys.stderr)
        return 64
    for name in ("paper-radar.out.log", "paper-radar.err.log"):
        rotate(root / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
