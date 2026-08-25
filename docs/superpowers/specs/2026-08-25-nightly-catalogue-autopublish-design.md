# Nightly candidate discovery and publication without an external LLM

## Goal

Run one autonomous, quality-gated candidate discovery update every night at
03:00 `Europe/Warsaw`. The job must research configured public sources, apply
the repository's existing deterministic filters, update the candidate queue,
and commit and push directly to `main` only after all checks pass.

The workflow must never force-push, publish a partial discovery result,
bulk-refresh existing metadata, or add AI attribution trailers to commits. It
must never automatically accept a candidate into the public catalogue.

## Scope

The change converts the scheduled candidate discovery in `discover.yml` from
an automated pull request into a direct, validated update of
`.catalog/data/candidates.csv`. The weekly `refresh.yml` metadata review stays
separate and retains its pull-request flow.

The implementation will:

- modify the existing `discover.yml` workflow rather than introduce a second
  discovery workflow;
- add a strict `--fail-on-source-error` option to `discover_candidates.py`, so
  scheduled direct publication cannot commit partial source results, including
  a failed repository lookup discovered through a Telegram source;
- add focused tests for that option and the allowed-file gate;
- document the schedule and no-API behaviour.

No OpenAI API, OpenAI account, paid service, additional secret, or new Python
dependency is needed. The workflow uses the existing GitHub-provided
`GITHUB_TOKEN` for GitHub requests and push authentication.

## Schedule and triggering

GitHub Actions cron is UTC-only. To achieve 03:00 in Warsaw across daylight
saving transitions, the workflow schedules both `01:00 UTC` and `02:00 UTC`.
It evaluates `TZ=Europe/Warsaw date +%H` before discovery and skips successfully
unless the local hour is `03`. This yields one nightly execution:

- CET: `02:00 UTC` -> 03:00 Warsaw;
- CEST: `01:00 UTC` -> 03:00 Warsaw.

`workflow_dispatch` bypasses the time guard for a deliberate manual run. A
single concurrency group prevents overlapping manual and scheduled discovery
runs and never cancels an active run.

## Candidate discovery pipeline

1. Check out `main` with full history and fetch it before beginning the scan.
2. When the existing `automation/catalog-candidates` branch is available,
   extract its candidate CSV as a seed. This preserves the candidate queue from
   the currently open review pull request. The workflow does not close that
   pull request or delete its branch.
3. Run the existing `discover_candidates.py --write` against the configured
   GitHub, GitLab, Codeberg, MCP Registry, and Telegram sources with its current
   14-day lookback, 100-result source cap, and request delay. The seed is merged
   by canonical repository URL.
4. Keep the current deterministic discovery rules:

   - skip archived repositories and repositories already present in either the
     canonical catalogue or candidate queue;
   - require valid lifecycle dates and activity no older than the catalogue's
     `MIN_LAST_UPDATE` policy;
   - derive score and confidence from the existing OSINT relevance terms,
     topics, source suggestions, available language and size signals, license
     metadata, and popularity metadata;
   - preserve source-provided suggested category, target inputs, views,
     description, metadata, and evidence in the candidate record.

   These records retain `Review Status: review`. A score, source suggestion, or
   candidate confidence is not an automatic acceptance decision.
5. Use `--fail-on-source-error` in the scheduled workflow. A failed source,
   failed downstream repository lookup, malformed response, or rate-limit
   error fails the job before staging, so a partial candidate queue is never
   pushed to `main`.
6. Run the catalogue gate before every possible commit:

   ```bash
   python -m py_compile .catalog/scripts/*.py
   python .catalog/scripts/render_catalog.py --check
   python .catalog/scripts/validate_catalog.py
   git diff --check
   ```

7. Enforce an allowed-file gate. The only tracked file a nightly discovery run
   may modify or stage is:

   ```text
   .catalog/data/candidates.csv
   ```

   A change to `osint-repositories.csv`, a generated public view, a workflow,
   script, or any other tracked file fails the job before staging.
8. Commit only a non-empty staged change using the existing GitHub Actions bot
   identity and the message:

   ```text
   chore: discover OSINT candidates
   ```

   Fetch `origin/main`, rebase the fresh commit onto it, rerun the static gate,
   and push `HEAD:main` without force. A moved remote or rebase conflict fails
   safely without a push.
9. Verify the pushed result with `git rev-parse HEAD` and
   `git ls-remote origin refs/heads/main`, then write the candidate count and
   commit SHA to the GitHub Actions job summary.

## Commit identity and audit trail

The workflow uses `github-actions[bot]` and does not add `Co-authored-by`,
Codex, or AI trailers. Candidate records retain discovery date, source, query,
suggested fields, metadata, evidence, score, confidence, review status, and
notes. They are therefore auditable and ready for ordinary curated review.

## Error handling

- A source, GitHub request, or public-source API failure: report the failed
  source and publish nothing.
- No newly discovered candidate: exit successfully without creating a commit.
- Validation, allowed-file, rebase, or push failure: publish nothing and do
  not retry with force.
- Missing write permission for `GITHUB_TOKEN`: fail before a push and publish
  nothing.

## Required repository setup

No secret needs to be added. The workflow requests `contents: write`, which is
sufficient with the repository's existing Actions setting.
The existing `GITHUB_TOKEN` is created automatically for every workflow run;
it is not a personal access token and has no separate cost or configuration.

## Verification strategy

- Unit tests cover strict failure on any source error and the single-file
  staging gate.
- The existing Python compilation, renderer check, catalogue validator, and
  whitespace gate run inside the workflow before every possible commit and
  again after a rebase.
- A manual `workflow_dispatch` validates time-guard bypass, a no-op run, a
  candidate update, direct-main push, and the post-push Git SHA comparison.
- The workflow is checked with `actionlint` when available. It does not rely on
  a bot-originated push to trigger `validate.yml`.

## Non-goals

- No automatic acceptance or rejection of candidates.
- No bulk star, date, snapshot, or existing-row metadata refresh.
- No automatic execution of third-party repositories.
- No force-push, branch deletion, pull-request auto-merge, or external
  notification system.
