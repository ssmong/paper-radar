# Paper Radar

An interactive survey of contact-rich dexterous manipulation, with arXiv discovery, automatic publication, and owner-controlled removal through Slack.

**Browse:** [English](https://ssmong.github.io/paper-radar/) · [한국어](https://ssmong.github.io/paper-radar/ko/) · [中文](https://ssmong.github.io/paper-radar/zh/)

The site has searchable tables, hand-type and year filters, paper detail pages, and OpenReview data where available. Browsing requires no installation.

## What runs where

| Component | Current setup |
| --- | --- |
| Public website | GitHub Pages serves `main:/docs` |
| Daily discovery and AI processing | Your Mac mini, at **08:30 in the Mac's local time zone** |
| Default AI backend | Codex CLI with the operating user's saved ChatGPT login |
| Publication | AI-accepted candidates are checked, built, tested, and pushed automatically |
| Later removal | The owner clicks **거부 · 사이트에서 삭제** in Slack |
| Slack button receiver | A separate Mac background service using Socket Mode |
| GitHub Actions paper discovery | Manual, deterministic recovery only; no daily schedule or Slack notification |
| Claude Code subscription backend | **Not implemented yet**; the optional `anthropic` backend uses an API key |

**Deploying this repository to GitHub does not install or start the Mac services.** Complete the setup below on the Mac that will run them.

## Quick start: daily automation on a Mac

### 1. Prepare the machine and repository

You need Python **3.10+**, Git, a recent Codex CLI, a Slack workspace where you can install the app, and Git credentials that can push to this repository's `main` branch. Use one macOS account for setup and scheduled execution.

For a new checkout:

```zsh
git clone https://github.com/ssmong/paper-radar.git
cd paper-radar
```

For an existing installation, use [Updating an existing Mac](#updating-an-existing-mac) below. If using your own fork, clone that fork and enable GitHub Pages from `main`, `/docs` in its repository settings. The publisher uses the checkout's `origin` remote.

Verify Python, your Git commit identity, and Codex login:

```zsh
python3 --version
git var GIT_AUTHOR_IDENT
codex login
codex login status
python3 scripts/codex_batch_classifier.py --preflight-only
```

If Git reports a missing identity, set your own `user.name` and `user.email` with `git config`. Configure Git authentication before scheduling; fetching a public repository alone does not prove that you have push access. Branch rules must permit the publisher's direct pushes. See the [operator guide](docs/mac-mini-codex-operator-guide.md#1-prepare-codex-and-git-on-the-mac-mini).

### 2. Check the project without network or AI usage

```zsh
python3 -m unittest discover -s tests -q
python3 build.py
python3 -m scripts.paper_loop run \
  --fixture tests/fixtures/arxiv_sample.xml \
  --now 2026-08-25T00:00:00Z \
  --no-llm --dry-run
```

This checks the local pipeline without sending Slack messages or publishing papers. `--dry-run` alone still permits arXiv requests and AI usage; the fixture and `--no-llm` make this particular command offline.

### 3. Connect Slack

Create or update the Slack app using [slack-app-manifest.yml](slack-app-manifest.yml). Install it in the workspace, keep **Socket Mode** and **Interactivity** enabled, and invite `@Paper Radar` to the destination channel.

Collect these four values. The [Slack setup instructions](docs/mac-mini-codex-operator-guide.md#2-create-the-slack-app) explain where to get them.

| Value | Purpose |
| --- | --- |
| Bot token (`xoxb-…`) | Send messages |
| App-level token (`xapp-…`, `connections:write`) | Receive button clicks |
| Destination conversation ID | Where the digest is sent |
| Your Slack member ID | Who may delete papers; this is not the destination ID |

Store them in Login Keychain. Each command prompts for its value:

```zsh
security add-generic-password -U -a "$USER" -s paper-radar-slack-bot-token -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-app-token -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-channel-id -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-approver-user-id -w
```

The last service retains its historical name, but now identifies the owner allowed to **reject and delete**. Do not put tokens in committed files. Installing the Slack app alone does not start daily delivery.

### 4. Install the daily job and button receiver

From the repository root:

```zsh
/bin/zsh scripts/macos/install_launch_agent.sh "$PWD"
```

The installer creates `.venv`, installs the Slack dependency, captures the Codex executable path, and loads two LaunchAgents:

- `com.ssmong.paper-radar`: discovery, automatic publication, and Slack delivery at 08:30.
- `com.ssmong.paper-radar-slack`: stays connected to Slack for removal clicks.

If the installer selects the wrong Python, rerun it with `PAPER_RADAR_PYTHON` set to the absolute path of Python 3.10+. `PAPER_RADAR_CODEX` can likewise select an absolute Codex executable path.

**To run the real daily job now**, use:

```zsh
launchctl kickstart "gui/$(id -u)/com.ssmong.paper-radar"
```

This uses your Codex allowance, can push papers to `main`, and sends Slack messages. It is not a preview. Do not start another copy while a run is active.

### 5. Check delivery and use the deletion button

```zsh
launchctl print "gui/$(id -u)/com.ssmong.paper-radar"
launchctl print "gui/$(id -u)/com.ssmong.paper-radar-slack"
tail -n 100 ~/Library/Logs/paper-radar/paper-radar.out.log
tail -n 100 ~/Library/Logs/paper-radar/paper-radar.err.log
tail -n 100 ~/Library/Logs/paper-radar/paper-radar-slack.err.log
```

The normal flow is:

**arXiv discovery → AI review → validated site update → Slack digest → optional owner rejection**

No approval click is needed to receive a message or publish an accepted paper. Uncertain candidates remain unpublished. Missing full text or failed publication checks are reported as failures and retried on the next automatic run.

Each Slack message contains up to six candidates; additional messages include the rest. **거부 · 사이트에서 삭제** removes the recorded rows and new detail pages for that paper, rebuilds the site, and blocks automatic republication. Only the configured owner can use it. Removal appears after GitHub Pages finishes deployment.

Papers added before publication records existed require manual removal. If someone has since edited a recorded row or detail file, automatic deletion stops instead of deleting that edited content. Removal changes the current site; earlier versions remain in Git history.

## Mac sleep and common problems

Keep the Mac awake, its user session logged in, and required keychain entries accessible during a daily run or deletion click. Screen locking is compatible with background execution when credentials remain accessible. System sleep stops the work; this installer does not configure wake schedules or prevent sleep. After a restart, log in before relying on these per-user services.

| Symptom | Check |
| --- | --- |
| Slack app installed, but no daily messages | Install the Mac services, then inspect the daily job log. The GitHub recovery workflow does not send Slack messages. |
| A successful run sends no digest | With `slack.notify_when_empty: false`, a run with no analyzed papers is silent. Check the output log and state. |
| Slack delivery fails | Check bot token, destination conversation ID, and channel invitation. Failed messages remain in the outbox. |
| Delete button does not respond | Check that the Mac is awake and the Slack listener is running; verify Socket Mode, Interactivity, and app token. |
| Delete button says you lack permission | Check the configured Slack member ID. |
| Publication or deletion fails | Inspect logs and run reports. Check Git push access, full text, unchanged recorded content, and whether another publication is in progress. |
| Codex authentication fails | Run `codex login` as the operating user, then repeat the preflight. |

See the [operator guide](docs/mac-mini-codex-operator-guide.md) for detailed setup and recovery.

## Updating an existing Mac

Wait for any active discovery or deletion job to finish. From the existing repository root, stop both services, pull, and reinstall them:

```zsh
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar.plist"
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar-slack.plist"
git pull --ff-only
/bin/zsh scripts/macos/install_launch_agent.sh "$PWD"
```

A service that is not installed can report an error during `bootout`. If the pull fails, resolve that first before reinstalling. Preserve local run reports, feedback, state, and the outbox; do not discard them to force an update. Reinstalling restarts the listener so it loads the new code.

To stop automation without uninstalling files, run only the two `bootout` commands above.

## Configuration and stored data

Edit [automation/paper-loop.json](automation/paper-loop.json) to change queries, classification thresholds, analysis limits, and Slack behavior. The default pipeline classifies up to 60 abstracts and performs detailed insight analysis for up to eight candidates. Automatic publication also fetches full text for each accepted paper, so it can use additional AI time.

| Path | Contents |
| --- | --- |
| `content/` | English, Korean, and Chinese survey sources and paper details |
| `reviews/` | OpenReview data |
| `docs/` | Generated public site and operator guide |
| `automation/inbox/latest.md` | Latest discovery report |
| `automation/runs/` | Run records needed for publication retries and later deletion |
| `automation/drafts/` | Drafts for AI-accepted candidates |
| `automation/state.json` | Processed, seen, and pending paper IDs |
| `automation/review_decisions.jsonl` | Local human feedback |
| `automation/outbox/slack/` | Messages retained until successful delivery |
| `automation/publications/` | Committed addition records and rejection records |

Manual CLI runs publish only when `--auto-publish --notify-slack` is supplied with an LLM backend and Slack enabled. The Mac runner supplies these flags and loads Slack values from Keychain. Deterministic runs cannot auto-publish.

The [paper discovery workflow](.github/workflows/paper-loop.yml) is a manual recovery tool. It uses deterministic classification and can create a draft review PR. It does not run daily, use your Codex login, send Slack digests, or publish papers. GitHub Pages deployment runs separately after a push to the site source.

## Build or edit the website locally

A static preview needs only Python:

```zsh
python3 build.py
python3 -m http.server 5500 --directory docs
```

Open [localhost:5500](http://localhost:5500). For automatic rebuild and browser refresh, install the optional `livereload` dependency in a virtual environment and run `python3 scripts/serve.py`.

## Author

Yeonseo Lee · Seoul National University
