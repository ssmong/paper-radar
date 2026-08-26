# Survey: Contact-Rich Dexterous Manipulation

An interactive survey of 150+ papers on contact-rich dexterous manipulation, covering RL-based methods, vision-language-action models, force-aware control, teleoperation, tactile sensing, and dexterous hand hardware.

**Live site:** https://ssmong.github.io/survey-contact-rich-dexterous-manipulation/

Available in English, [Korean](https://ssmong.github.io/survey-contact-rich-dexterous-manipulation/ko/), and [Chinese](https://ssmong.github.io/survey-contact-rich-dexterous-manipulation/zh/).

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
6. write a review report and candidate drafts without editing the survey.

Classification is abstract-grounded. High-confidence candidates still arrive
in a draft pull request and require a human to verify the full paper before any
survey content is changed.

### Run locally

The loop uses only the Python standard library. Set `ANTHROPIC_API_KEY` to use
the configured Claude model:

```bash
python scripts/paper_loop.py run --dry-run
python scripts/paper_loop.py run
```

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
- `automation/state.json`: processed paper IDs and the persistent pending queue.

`max_candidates_per_run` caps LLM cost. Reports show both the number that
passed the prefilter and the number classified in the current run, so a backlog
is visible rather than silently hidden. Unprocessed recent candidates remain
in the pending queue for a later run, even after they age past the arXiv
lookback window.

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

### Scheduled pull requests

`.github/workflows/paper-loop.yml` runs every Monday at 10:23 KST and can also
be started manually from the Actions tab. It runs the offline tests, checks the
Python files, verifies `build.py`, executes one live discovery cycle, and
creates or updates a draft PR containing only `automation/` artifacts.

Repository setup:

1. Add an Actions secret named `ANTHROPIC_API_KEY` for LLM classification.
   Without it, the scheduled job safely falls back to heuristic review-only
   classification.
2. Optionally set the Actions variable `ANTHROPIC_MODEL` to override the model
   in `automation/paper-loop.json`. `ANTHROPIC_BASE_URL` is also supported for
   an API-compatible gateway.
3. In **Settings → Actions → General → Workflow permissions**, allow GitHub
   Actions to create pull requests and grant read/write workflow permissions.

The workflow keeps one fixed automation branch, so an open review PR is updated
instead of creating duplicate PRs on every schedule.

## Author

Yeonseo Lee · Seoul National University
