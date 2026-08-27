#!/bin/zsh
# Render and load the per-user LaunchAgent. Run this script interactively once.
set -euo pipefail
umask 077

export PATH="/usr/bin:/bin:/usr/sbin:/sbin"
readonly SCRIPT_DIR="${0:A:h}"
readonly REPO_ROOT="${1:-${SCRIPT_DIR:h:h}}"
readonly TEMPLATE="$SCRIPT_DIR/com.ssmong.paper-radar.plist.example"
readonly AGENT_DIR="$HOME/Library/LaunchAgents"
readonly LOG_DIR="$HOME/Library/Logs/paper-radar"
readonly TARGET="$AGENT_DIR/com.ssmong.paper-radar.plist"
readonly DOMAIN="gui/$(/usr/bin/id -u)"

if [[ -n "${PAPER_RADAR_PYTHON:-}" ]]; then
  readonly PYTHON_BIN="$PAPER_RADAR_PYTHON"
elif [[ -x /opt/homebrew/bin/python3 ]]; then
  readonly PYTHON_BIN=/opt/homebrew/bin/python3
elif [[ -x /usr/local/bin/python3 ]]; then
  readonly PYTHON_BIN=/usr/local/bin/python3
else
  readonly PYTHON_BIN=/usr/bin/python3
fi

if [[ "$REPO_ROOT" != /* || ! -d "$REPO_ROOT/.git" ]]; then
  print -u2 -- "usage: $0 /absolute/path/to/repository"
  exit 64
fi
if [[ ! -x "$PYTHON_BIN" ]]; then
  print -u2 -- "Python is not executable: $PYTHON_BIN"
  exit 69
fi
if ! "$PYTHON_BIN" -c \
  'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  print -u2 -- "Python 3.10 or newer is required: $PYTHON_BIN"
  exit 69
fi
/bin/zsh -n "$SCRIPT_DIR/run_paper_radar.sh" "$0"

/bin/mkdir -p "$AGENT_DIR" "$LOG_DIR"
"$PYTHON_BIN" - "$TEMPLATE" "$TARGET" "$REPO_ROOT" "$PYTHON_BIN" "$LOG_DIR" <<'PY'
import sys
from pathlib import Path

template, target, repo_root, python_bin, log_dir = sys.argv[1:]
text = Path(template).read_text(encoding="utf-8")
text = text.replace("__REPO_ROOT__", repo_root)
text = text.replace("__PYTHON_BIN__", python_bin)
text = text.replace("__LOG_DIR__", log_dir)
Path(target).write_text(text, encoding="utf-8")
PY
/bin/chmod 600 "$TARGET"
/usr/bin/plutil -lint "$TARGET"

/bin/launchctl bootout "$DOMAIN" "$TARGET" 2>/dev/null || true
/bin/launchctl bootstrap "$DOMAIN" "$TARGET"
/bin/launchctl enable "$DOMAIN/com.ssmong.paper-radar"
print -- "Installed $TARGET"
print -- "Run now: launchctl kickstart -k $DOMAIN/com.ssmong.paper-radar"
