# Survey: Contact-Rich Dexterous Manipulation

An interactive survey of 150+ papers on contact-rich dexterous manipulation, covering RL-based methods, vision-language-action models, force-aware control, teleoperation, tactile sensing, and dexterous hand hardware.

**Live site:** https://ssmong.github.io/paper-radar/

Available in English, [Korean](https://ssmong.github.io/paper-radar/ko/), and [Chinese](https://ssmong.github.io/paper-radar/zh/).

## Features

- Filterable and sortable tables with global search
- Per-paper detail pages with method summaries
- OpenReview peer review data (where available)
- Hand type filters (Dexterous, Gripper, Bimanual, Full Body)
- Dark / light theme toggle
- Responsive layout

## Structure

```
build.py            # Markdown → HTML build script
content/            # Survey source files (EN/KO/ZH)
  survey.md
  detailed/         # Per-paper detail pages
reviews/            # OpenReview data
scripts/            # Dev utilities (serve, fetch_reviews)
automation/         # Paper discovery configuration, state, reports, and drafts
docs/               # Generated site (GitHub Pages)
```

## Building

```bash
python build.py
```

## Local dev server

```bash
pip install livereload
python scripts/serve.py
```

## Automated paper discovery loop

The repository includes a conservative discovery and classification loop for
new arXiv papers. It is designed as a review assistant, not an unattended
publisher:

1. query arXiv for recent papers in the configured topic families;
2. deduplicate by arXiv ID and normalized title against `content/`, prior runs,
   and recorded human decisions;
3. apply a cheap keyword prefilter;
4. classify title and abstract, then run a skeptical second LLM review;
5. run a third adjudication pass when the first two disagree;
6. inspect arXiv HTML for the highest-priority papers and extract a grounded
   problem, method, contribution, limitation, and gap candidate;
7. calculate numeric deltas in Python only when the paper reports proposed and
   baseline values under matching task, dataset, metric, and evaluation
   conditions;
8. write a review report and candidate drafts without editing the survey.

Classification is abstract-grounded. High-confidence candidates still arrive
in a draft pull request and require a human to verify the full paper before any
survey content is changed.

### Run locally

The default backend is the locally installed Codex CLI with saved ChatGPT
authentication. Sign in once as the operating user and verify the saved session:

```bash
codex login
python scripts/codex_batch_classifier.py --preflight-only
python scripts/paper_loop.py run --llm-provider codex --dry-run
python scripts/paper_loop.py run --llm-provider codex --notify-slack
```

Codex receives bounded paper batches in an isolated temporary directory with an
ephemeral session, a read-only sandbox, and strict output schemas. Missing IDs,
invalid sections, unsupported evidence, authentication failures, and timeouts
fail closed; affected papers remain queued for retry instead of being recorded
as completed.

Use the deterministic fallback for a zero-cost check. It never auto-accepts a
paper and labels every matching item `needs_review`:

```bash
python scripts/paper_loop.py run --no-llm --dry-run
```

An offline fixture is available for repeatable development without network or
API access:

```bash
python scripts/paper_loop.py run \
  --fixture tests/fixtures/arxiv_sample.xml \
  --now 2026-08-25T00:00:00Z \
  --no-llm --dry-run
python -m unittest discover -s tests -v
```

Configuration lives in `automation/paper-loop.json`. The generated artifacts
are:

- `automation/inbox/latest.md`: the current human-review queue;
- `automation/runs/<timestamp>.json`: an auditable machine-readable run;
- `automation/drafts/section*/`: drafts only for candidates accepted by the
  LLM review loop;
- `automation/state.json`: processed, seen, and persistent pending paper IDs;
- `automation/outbox/slack/`: durable Slack payloads retained after delivery
  failures and replayed without consuming the paper queue.

The default configuration collects multiple pages from broad control and
robotics queries, ranks and batch-classifies up to 60 abstracts, then performs
full-text analysis only for the top eight reviewable papers. It first tries
arXiv HTML and falls back to the abstract when full text is unavailable. Source text is
numbered before LLM analysis, and every insight or numeric comparison must cite
its `[L####]` evidence locator. The model returns the reported proposed and
baseline values; Python recomputes the absolute difference and relative
improvement. A mismatch in task, dataset, metric, or evaluation condition is
shown as `comparison deferred` rather than converted into a misleading delta.

The Slack message contains the daily counts and up to six review priorities.
When full-text insight is available, each item shows the research problem,
method, contribution over prior work, tentative gap, and up to two numeric
comparisons. It links to the analyzed source and explicitly retains the
full-paper verification requirement.

Each candidate has owner-only `승인 후 반영` and `제외` buttons.

Approval is received through Slack Socket Mode on the Mac mini, so GitHub Pages remains a static output host and no public callback server is required.

An approved paper is edited in an isolated worktree and pushed only after full-text retrieval, generated-site build, unit tests, arXiv-ID verification, and changed-path checks succeed.

`max_candidates_per_run` and `screening.max_abstracts_per_run` bound batch
classification; `analysis.max_papers_per_run` separately bounds expensive
full-text analysis. Reports expose collected, prefiltered, classified,
deep-analyzed, deferred, backlog, and retryable-failure counts. Unprocessed
candidates remain in the pending queue even after they age past the arXiv
lookback window. Prefiltered-out and out-of-lookback IDs are also recorded so
the same papers are not counted as new every day.

After checking a paper, record the decision so later LLM passes can use it as a
calibration example:

```bash
python scripts/paper_loop.py review \
  --paper-id 2608.00001 \
  --decision accept \
  --section-id 5 \
  --note "Verified from full text"
```

For a rejection, use `--decision reject`; the section is stored as `0`.

### Mac mini scheduling and manual recovery

The supported daily scheduler is a single-user Mac mini LaunchAgent. It runs at
08:30 local time, retrieves Slack credentials from Login Keychain, checks Codex
authentication, prevents overlapping runs, and rotates bounded logs. Follow
[`docs/mac-mini-codex-operator-guide.md`](docs/mac-mini-codex-operator-guide.md)
for the one-time install, security model, preflight, inspection, and removal
commands.

`.github/workflows/paper-loop.yml` has no cron. It is a manually triggered,
deterministic recovery path only, so GitHub Actions cannot race the Mac, consume
its retry queue, or silently substitute heuristic results before Codex sees a
paper. Its outputs remain human-review artifacts and never edit published survey
content directly.

## Author

Yeonseo Lee · Seoul National University
