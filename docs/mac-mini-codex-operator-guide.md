# Mac mini: Codex + Slack paper radar

This path is for a trusted, single-user Mac mini. It uses the local Codex CLI's
saved ChatGPT authentication. It does **not** turn a ChatGPT subscription into an
OpenAI API key and should not be copied to a public runner. OpenAI recommends API
keys as the simpler default for general automation; this account-auth path is a
deliberate choice for the owner's trusted local machine.

Official references:

- [Codex authentication](https://developers.openai.com/codex/auth/)
- [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive/)

The adapter uses `codex exec` with an ephemeral session, an explicit read-only
sandbox, an isolated temporary working directory, and `--output-schema`. The
final JSON is still validated locally for exact paper-ID coverage and valid
survey sections. A missing ID, timeout, authentication failure, or invalid result
fails closed; the main loop should mark the affected candidates `needs_review`.

Each run first batch-classifies every broadly screened abstract (up to the
configured broad-screen limit). It then ranks those results and deep-analyzes only
the configured top set. Deep analysis uses numbered full-text lines, rejects
unknown locators, and never computes numerical improvements in the model; the
paper loop recomputes comparable deltas after validation.

## 1. One-time prerequisites

Install a recent Codex CLI and Python 3, then sign in interactively as the same
macOS user that will own the LaunchAgent:

```zsh
codex login
codex login status
```

ChatGPT sign-in opens a browser. Saved credentials are reused by `codex exec`.
Prefer the macOS credential store by adding this to `~/.codex/config.toml` before
login:

```toml
cli_auth_credentials_store = "keyring"
```

Do not copy `~/.codex/auth.json`, commit it, or share it. If the machine cannot
use Keychain, treat that file exactly like a password and keep it user-readable
only.

Verify the repository-side preflight:

```zsh
python3 scripts/codex_batch_classifier.py --preflight-only
```

The scheduled adapter intentionally ignores user Codex configuration and project
execution rules during inference, requests a read-only sandbox, and runs in a
fresh temporary working directory instead of the repository. It receives only an
allowlisted local environment; `SLACK_WEBHOOK_URL`, GitHub tokens, Anthropic keys,
OpenAI API keys, and unrelated project secrets are not passed to Codex. Read-only
is not a confidentiality boundary: the agent can invoke read-only tools and keeps
the real user context needed for saved authentication, so it may be able to read
other local files. The prompt therefore treats papers as untrusted data and
forbids tool and file access. Limit this design to the owner's trusted machine,
keep unrelated secrets out of that macOS account, and review every output.

## 2. Put the Slack webhook in Login Keychain

Create a Slack Incoming Webhook, then store it without writing it into the repo,
plist, command line, or logs:

```zsh
security add-generic-password -U \
  -a "$USER" \
  -s paper-radar-slack-webhook \
  -w
```

The command securely prompts for the webhook value. Test retrieval without
printing it:

```zsh
security find-generic-password \
  -a "$USER" \
  -s paper-radar-slack-webhook \
  -w >/dev/null
```

The Login Keychain normally must be unlocked. Run the job once while logged in
and approve Keychain access if macOS asks. The wrapper fetches the webhook only
for the parent paper-loop process, scrubs it from the Codex child environment,
and unsets it on exit.

## 3. Test one complete run

From the repository root:

```zsh
PAPER_RADAR_REPO_ROOT="$PWD" \
  /bin/zsh scripts/macos/run_paper_radar.sh
```

The wrapper refuses to continue unless the main loop exposes
`--llm-provider codex`. It also uses a stale-safe per-user lock, so overlapping scheduled
runs do not corrupt the queue. On failure it sends a short Slack alert and puts
diagnostics in the error log without including credentials or the webhook URL.
Logs rotate at 2 MiB with two retained generations.

## 4. Install the 08:30 LaunchAgent

Use an absolute repository path:

```zsh
/bin/zsh scripts/macos/install_launch_agent.sh "$PWD"
```

The installer requires Python 3.10 or newer, syntax-checks both zsh scripts, then
renders a user-only plist at
`~/Library/LaunchAgents/com.ssmong.paper-radar.plist` and stores logs under
`~/Library/Logs/paper-radar/`. It never places a secret in the plist.

Trigger and inspect it:

```zsh
launchctl kickstart -k "gui/$(id -u)/com.ssmong.paper-radar"
launchctl print "gui/$(id -u)/com.ssmong.paper-radar"
tail -n 100 ~/Library/Logs/paper-radar/paper-radar.err.log
```

`launchd` runs missed calendar jobs when the Mac becomes available, but it cannot
run code while the Mac is powered off. Keep the Mac awake at the scheduled time
or configure an appropriate macOS wake schedule separately. The user session and
Login Keychain must be available.

After an unclean shutdown, an empty stale lock can remain. If no paper-radar
process is running, remove only that exact per-user directory and retry:

```zsh
rmdir "${TMPDIR:-/tmp}/paper-radar-$(id -u).lock"
```

## 5. Operating and recovery rules

- Keep the default Codex model unless a tested model is explicitly required.
  `PAPER_RADAR_CODEX_MODEL` can pin one, but availability follows the signed-in
  ChatGPT workspace.
- Treat subscription limits, expired login, timeouts, invalid structured output,
  and missing batch items as recoverable failures. Do not auto-accept a heuristic
  substitute; leave candidates queued or mark them for human review.
- If preflight fails, run `codex login` interactively again. Codex normally
  refreshes active ChatGPT sessions, but reauthentication can still be required.
- Rotate a leaked Slack webhook in Slack and replace the Keychain item. Never
  paste the old webhook into an issue, log, PR, or chat.
- Review `automation/inbox/latest.md` and generated drafts before merging. The
  model narrows the reading queue; it does not establish publication facts.

To unload the scheduler without deleting its plist:

```zsh
launchctl bootout "gui/$(id -u)" \
  "$HOME/Library/LaunchAgents/com.ssmong.paper-radar.plist"
```
