# Mac mini paper radar: Codex, automatic publication, and Slack removal

This setup keeps discovery, Codex, Slack interaction, and Git publishing on one trusted Mac mini.

GitHub Pages only serves the generated static site and never receives Slack callbacks or secrets.

The daily process is `Mac mini discovery → AI acceptance → isolated survey edit → build and tests → git push → Slack notification`. The owner can later reject a paper in Slack to remove it from GitHub Pages.

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

The automatic publisher pushes directly to `main`, so the account must have push permission and branch rules must allow that push.

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

Only the Slack member ID stored as `paper-radar-slack-approver-user-id` can reject and remove a paper. The existing keychain service name is retained for compatibility.

## 4. Install both LaunchAgents

Run the installer from the repository root with an absolute path.

```zsh
/bin/zsh scripts/macos/install_launch_agent.sh "$PWD"
```

The installer creates `.venv`, installs Slack Bolt, and installs two per-user LaunchAgents.
It also records the absolute `codex` path from the interactive shell, so standalone installs such as `~/.local/bin/codex` work under launchd.

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

The Login Keychain must be unlocked and the Mac must be running for discovery and Slack removal clicks to work. A locked screen is different from system sleep; keep the login session active and check that keychain reads work unattended.

## 5. Automatic publication and later rejection

The daily runner passes `--auto-publish --notify-slack`. Only AI-accepted candidates without classification errors enter publication. Uncertain results are still sent to Slack, without publishing them.

For each accepted paper, the publisher fetches full arXiv HTML, edits an isolated worktree based on the latest remote branch, and validates one inserted table row per language. Existing content must stay unchanged. Build and unit tests must pass before it pushes. Publication failures remain in the saved run report and retry on the next automatic daily run.

Slack reports the publication status and provides `거부 · 사이트에서 삭제`. No approval click is required to publish. Digest pagination keeps a deletion button available for every paper.

Clicking reject removes exactly the recorded rows and new detail pages, rebuilds the site, and commits a persistent rejection record. It does not use an LLM to choose what to delete. Repeated clicks are safe; rejected IDs cannot be published again automatically. If someone edited the recorded rows or detail files later, deletion stops with an error for manual resolution.

Only the configured owner can delete papers. Publication and deletion share a local process lock; a busy or failed deletion reports an error, and the original button remains available for retry. A concurrent remote update fails the push rather than overwriting it.

Keep local run reports in `automation/runs/`. The remote records in `automation/publications/` identify additions and rejected papers. Older papers without a publication record require manual removal. Removal affects the current site; Git history retains prior versions. The site changes after its normal deployment completes.

## 6. Limits and recovery

GitHub Pages cannot receive a Slack button callback because it is static hosting.

Socket Mode removes the need for a public server, tunnel, or callback URL while still requiring the Mac mini to stay online.

Daily AI work no longer consumes GitHub Actions minutes because it runs through the local Codex CLI.

If Codex authentication expires, run `codex login` interactively and restart the Slack listener.

If a paper lacks arXiv HTML, review it manually or add a trusted PDF extraction path before retrying.

If direct pushes are later disallowed, replace the final push with a pull-request branch while keeping the same publication validation and retraction records.

To unload both services, run these commands.

```zsh
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar.plist"
launchctl bootout "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.ssmong.paper-radar-slack.plist"
```
