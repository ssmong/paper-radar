#!/bin/zsh
# Trusted, single-user macOS runner. Secrets are fetched from Login Keychain and
# are deliberately not passed through to the Codex subprocess by the adapter.
set -euo pipefail
umask 077

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
readonly SCRIPT_DIR="${0:A:h}"
readonly DEFAULT_REPO_ROOT="${SCRIPT_DIR:h:h}"
readonly REPO_ROOT="${PAPER_RADAR_REPO_ROOT:-$DEFAULT_REPO_ROOT}"
readonly PYTHON_BIN="${PAPER_RADAR_PYTHON:-/usr/bin/python3}"
readonly CODEX_BIN_VALUE="${CODEX_BIN:-codex}"
readonly BOT_TOKEN_SERVICE="${PAPER_RADAR_SLACK_BOT_SERVICE:-paper-radar-slack-bot-token}"
readonly CHANNEL_SERVICE="${PAPER_RADAR_SLACK_CHANNEL_SERVICE:-paper-radar-slack-channel-id}"
readonly ACCOUNT_NAME="$(/usr/bin/id -un)"
readonly LOCK_DIR="${TMPDIR:-/tmp}/paper-radar-${UID}.lock"
readonly LOCK_PID_FILE="$LOCK_DIR/pid"
readonly LOG_DIR="${PAPER_RADAR_LOG_DIR:-$HOME/Library/Logs/paper-radar}"

if [[ ! -d "$REPO_ROOT/.git" || ! -f "$REPO_ROOT/scripts/paper_loop.py" ]]; then
  print -u2 -- "paper-radar: invalid absolute repository path: $REPO_ROOT"
  exit 64
fi
if [[ "$REPO_ROOT" != /* ]]; then
  print -u2 -- "paper-radar: PAPER_RADAR_REPO_ROOT must be absolute"
  exit 64
fi
if [[ ! -x "$PYTHON_BIN" ]]; then
  print -u2 -- "paper-radar: Python is not executable: $PYTHON_BIN"
  exit 69
fi
if ! "$PYTHON_BIN" -c \
  'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
  print -u2 -- "paper-radar: Python 3.10 or newer is required: $PYTHON_BIN"
  exit 69
fi

function acquire_lock {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    print -r -- "$$" > "$LOCK_PID_FILE"
    return 0
  fi
  if [[ -L "$LOCK_DIR" ]]; then
    print -u2 -- "paper-radar: refusing symlink lock path: $LOCK_DIR"
    return 1
  fi
  local prior_pid=""
  if [[ -r "$LOCK_PID_FILE" ]]; then
    read -r prior_pid < "$LOCK_PID_FILE" || prior_pid=""
  fi
  if [[ "$prior_pid" == <-> ]] && /bin/kill -0 "$prior_pid" 2>/dev/null; then
    print -u2 -- "paper-radar: active run pid=$prior_pid holds $LOCK_DIR"
    return 1
  fi
  /bin/rm -f -- "$LOCK_PID_FILE"
  if ! rmdir "$LOCK_DIR" 2>/dev/null || ! mkdir "$LOCK_DIR" 2>/dev/null; then
    print -u2 -- "paper-radar: stale lock could not be reclaimed: $LOCK_DIR"
    return 1
  fi
  print -r -- "$$" > "$LOCK_PID_FILE"
}

if ! acquire_lock; then
  exit 75
fi

function cleanup {
  local exit_code=$?
  if (( exit_code != 0 )) && [[ -n "${SLACK_BOT_TOKEN:-}" ]]; then
    "$PYTHON_BIN" "$REPO_ROOT/scripts/macos/notify_slack_failure.py" \
      "exit=$exit_code; inspect the launchd error log" || true
  fi
  unset SLACK_BOT_TOKEN SLACK_CHANNEL_ID
  local owner_pid=""
  if [[ -r "$LOCK_PID_FILE" ]]; then
    read -r owner_pid < "$LOCK_PID_FILE" || owner_pid=""
  fi
  if [[ "$owner_pid" == "$$" ]]; then
    /bin/rm -f -- "$LOCK_PID_FILE"
    rmdir "$LOCK_DIR" 2>/dev/null || true
  fi
  if [[ -d "$LOG_DIR" ]]; then
    "$PYTHON_BIN" "$REPO_ROOT/scripts/macos/rotate_logs.py" "$LOG_DIR" || true
  fi
  return $exit_code
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if [[ -z "${SLACK_BOT_TOKEN:-}" ]]; then
  SLACK_BOT_TOKEN="$(/usr/bin/security find-generic-password \
    -a "$ACCOUNT_NAME" -s "$BOT_TOKEN_SERVICE" -w 2>/dev/null)" || {
      print -u2 -- "paper-radar: Slack bot token missing from Login Keychain"
      exit 78
    }
  export SLACK_BOT_TOKEN
fi
if [[ -z "${SLACK_CHANNEL_ID:-}" ]]; then
  SLACK_CHANNEL_ID="$(/usr/bin/security find-generic-password \
    -a "$ACCOUNT_NAME" -s "$CHANNEL_SERVICE" -w 2>/dev/null)" || {
      print -u2 -- "paper-radar: Slack channel ID missing from Login Keychain"
      exit 78
    }
  export SLACK_CHANNEL_ID
fi

# Fail closed if the main loop has not been integrated with this backend. This
# avoids a scheduled run silently using heuristic or Anthropic classification.
cd "$REPO_ROOT"
if ! "$PYTHON_BIN" -m scripts.paper_loop run --help \
  | /usr/bin/grep -q -- "--llm-provider"; then
  print -u2 -- "paper-radar: main loop lacks required --llm-provider integration"
  exit 70
fi

export CODEX_BIN="$CODEX_BIN_VALUE"
"$PYTHON_BIN" "$REPO_ROOT/scripts/codex_batch_classifier.py" \
  --repo-root "$REPO_ROOT" \
  --codex-bin "$CODEX_BIN_VALUE" \
  --preflight-only >/dev/null

"$PYTHON_BIN" -m scripts.paper_loop \
  --repo-root "$REPO_ROOT" \
  run \
  --llm-provider codex \
  --notify-slack
