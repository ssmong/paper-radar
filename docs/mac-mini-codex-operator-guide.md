# Mac mini paper radar: Codex, Slack approval, and GitHub Pages

This setup keeps discovery, Codex, Slack interaction, and Git publishing on one trusted Mac mini.

GitHub Pages only serves the generated static site and never receives Slack callbacks or secrets.

The daily process is `Mac mini discovery → Slack candidates → owner approval → isolated survey edit → build and tests → git push → GitHub Pages`.

The GitHub Actions workflow remains a manual deterministic recovery path and is not used for daily AI work.

Official references:

- [Codex authentication](https://developers.openai.com/codex/auth/)
- [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive/)
- [Slack Socket Mode](https://api.slack.com/apis/connections/socket)
- [Slack Block Kit buttons](https://api.slack.com/block-kit/block-elements#button)
- [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## 1. Prepare Codex and git on the Mac mini

Install a recent Codex CLI, Python 3.10 or newer, and git.

Sign in to Codex as the same macOS user that will own the LaunchAgents.

```zsh
codex login
codex login status
python3 scripts/codex_batch_classifier.py --preflight-only
```

The saved ChatGPT login is reused by `codex exec` on this trusted machine and is not an OpenAI API key.

Prefer the macOS credential store by adding `cli_auth_credentials_store = "keyring"` to `~/.codex/config.toml` before login.

Configure the repository's normal git credential helper and verify that this command succeeds without embedding a token in the repository.

```zsh
git fetch origin main
```

The approval publisher pushes directly to `main`, so the account must have push permission and branch rules must allow that push.

## 2. Create the Slack App

Create an app at [Slack API Apps](https://api.slack.com/apps) and choose **From an app manifest**.

Paste [`slack-app-manifest.yml`](../slack-app-manifest.yml) into the manifest editor and create the app.

Install the app to the workspace from **OAuth & Permissions** and copy the Bot User OAuth Token beginning with `xoxb-`.

Create an app-level token from **Basic Information → App-Level Tokens** with the `connections:write` scope and copy the token beginning with `xapp-`.

Socket Mode and Interactivity must remain enabled.

Invite `@Paper Radar` to the target channel with `/invite @Paper Radar`.

Copy the target channel ID and your own Slack member ID from Slack's **View channel details** and **Copy member ID** menus.

The bot token and app token are the only API credentials.

The channel ID and approver member ID are identifiers rather than secrets, but this setup stores all four values in Login Keychain to keep launchd configuration uniform.

## 3. Store Slack values in Login Keychain

Each command securely prompts for one value and does not place it in shell history.

```zsh
security add-generic-password -U -a "$USER" -s paper-radar-slack-bot-token -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-app-token -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-channel-id -w
security add-generic-password -U -a "$USER" -s paper-radar-slack-approver-user-id -w
```

Verify only that the entries can be read without printing their contents.

```zsh
for service in \
  paper-radar-slack-bot-token \
  paper-radar-slack-app-token \
  paper-radar-slack-channel-id \
  paper-radar-slack-approver-user-id; do
  security find-generic-password -a "$USER" -s "$service" -w >/dev/null || exit 1
done
```

Only the Slack member ID stored as `paper-radar-slack-approver-user-id` can approve or reject a paper.

## 4. Install both LaunchAgents

Run the installer from the repository root with an absolute path.

```zsh
/bin/zsh scripts/macos/install_launch_agent.sh "$PWD"
```

The installer creates `.venv`, installs Slack Bolt, and installs two per-user LaunchAgents.

`com.ssmong.paper-radar` runs the daily discovery job at 08:30 local time.

`com.ssmong.paper-radar-slack` keeps the Socket Mode listener running so button clicks reach the Mac without a public callback URL.

Trigger one discovery run and inspect both services.

```zsh
launchctl kickstart -k "gui/$(id -u)/com.ssmong.paper-radar"
launchctl print "gui/$(id -u)/com.ssmong.paper-radar"
launchctl print "gui/$(id -u)/com.ssmong.paper-radar-slack"
tail -n 100 ~/Library/Logs/paper-radar/paper-radar.err.log
tail -n 100 ~/Library/Logs/paper-radar/paper-radar-slack.err.log
```

The Login Keychain must be unlocked and the Mac must be running for discovery and Slack approvals to work.

## 5. What happens after a button click

`제외` records a human rejection and prevents the same paper from reappearing as a new candidate.

`승인 후 반영` acknowledges the Slack action immediately and then serializes publication so two papers cannot be pushed at once.

The publisher fetches the full arXiv HTML and refuses to publish when only the abstract is available.

It creates a temporary git worktree from the latest `origin/main` and gives Codex only the approved paper source and target survey section.

Codex may edit only `content/`, and the process rejects any unexpected path.

The process then runs `python build.py`, executes the unit tests, verifies that the final diff is limited to `content/` and `docs/`, and checks that the approved arXiv ID is present.

Only after every check passes does it commit and push to `main`.

A concurrent remote update causes the push to fail rather than overwrite another change.

Slack shows `반영 완료` only after the push succeeds and restores the buttons with an error message when publication fails.

## 6. Limits and recovery

GitHub Pages cannot receive a Slack button callback because it is static hosting.

Socket Mode removes the need for a public server, tunnel, or callback URL while still requiring the Mac mini to stay online.

Daily AI work no longer consumes GitHub Actions minutes because it runs through the local Codex CLI.

If Codex authentication expires, run `codex login` interactively and restart the Slack listener.

If a paper lacks arXiv HTML, review it manually or add a trusted PDF extraction path before retrying.

If direct pushes are later disallowed, replace the final push with a pull-request branch while keeping the same Slack approval and validation steps.

To unload both services, run these commands.

```zsh
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar.plist"
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar-slack.plist"
```
