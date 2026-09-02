#!/bin/zsh
set -euo pipefail
umask 077

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
readonly SCRIPT_DIR="${0:A:h}"
readonly REPO_ROOT="${PAPER_RADAR_REPO_ROOT:-${SCRIPT_DIR:h:h}}"
readonly PYTHON_BIN="${PAPER_RADAR_BOT_PYTHON:-$REPO_ROOT/.venv/bin/python3}"
readonly ACCOUNT_NAME="$(/usr/bin/id -un)"
readonly BOT_TOKEN_SERVICE="${PAPER_RADAR_SLACK_BOT_SERVICE:-paper-radar-slack-bot-token}"
readonly APP_TOKEN_SERVICE="${PAPER_RADAR_SLACK_APP_SERVICE:-paper-radar-slack-app-token}"
readonly APPROVER_SERVICE="${PAPER_RADAR_SLACK_APPROVER_SERVICE:-paper-radar-slack-approver-user-id}"

if [[ "$REPO_ROOT" != /* || ! -d "$REPO_ROOT/.git" ]]; then
  print -u2 -- "paper-radar: invalid absolute repository path: $REPO_ROOT"
  exit 64
fi
if [[ ! -x "$PYTHON_BIN" ]]; then
  print -u2 -- "paper-radar: Slack bot environment is missing; rerun install_launch_agent.sh"
  exit 69
fi

function keychain_value {
  /usr/bin/security find-generic-password -a "$ACCOUNT_NAME" -s "$1" -w 2>/dev/null
}

SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN:-$(keychain_value "$BOT_TOKEN_SERVICE")}" || exit 78
SLACK_APP_TOKEN="${SLACK_APP_TOKEN:-$(keychain_value "$APP_TOKEN_SERVICE")}" || exit 78
SLACK_APPROVER_USER_ID="${SLACK_APPROVER_USER_ID:-$(keychain_value "$APPROVER_SERVICE")}" || exit 78
export SLACK_BOT_TOKEN SLACK_APP_TOKEN SLACK_APPROVER_USER_ID
trap 'unset SLACK_BOT_TOKEN SLACK_APP_TOKEN SLACK_APPROVER_USER_ID' EXIT

cd "$REPO_ROOT"
exec "$PYTHON_BIN" "$REPO_ROOT/scripts/slack_review_bot.py"
