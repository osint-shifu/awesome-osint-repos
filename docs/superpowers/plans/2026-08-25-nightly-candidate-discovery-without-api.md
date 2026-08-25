# Nightly Candidate Discovery Without API Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Run the existing candidate discovery pipeline exactly once at 03:00 Europe/Warsaw, commit only validated candidate-queue changes directly to main, and require no OpenAI API or user-managed secret.

**Architecture:** Candidate discovery and canonical curation stay separate. discover_candidates.py gains strict source-error behavior so scheduled runs never write or publish a partial result. A small standard-library changed-file checker makes the direct-main staging rule testable, while discover.yml handles scheduling, legacy candidate preservation, validation, rebase, and non-force push.

**Tech Stack:** Python 3.12 standard library, unittest, GitHub Actions, Git, existing GitHub-provided GITHUB_TOKEN.

**Spec:** docs/superpowers/specs/2026-08-25-nightly-catalogue-autopublish-design.md

## Global Constraints

- Run exactly once at 03:00 Europe/Warsaw, including CET and CEST.
- Use no OpenAI API, OpenAI secret, paid service, new dependency, or personal access token.
- Keep candidates at Review Status: review. Never automatically accept or reject canonical catalogue entries.
- Preserve automation/catalog-candidates and its open pull request without closing or deleting either.
- The nightly workflow may modify and stage only .catalog/data/candidates.csv.
- Keep refresh.yml as the separate weekly pull-request metadata workflow.
- Never force-push or publish after a source, validation, allowlist, rebase, or push error.
- Use github-actions[bot] without Codex, AI, or Co-authored-by trailers.
- Do not run, install, import, or clone third-party candidate code.

## File Structure

| Path | Responsibility |
|---|---|
| .catalog/scripts/discover_candidates.py | Discover candidates and expose strict source-error behavior. |
| .catalog/scripts/check_changed_files.py | Testable standard-library allowlist gate for changed tracked paths. |
| tests/test_discover_candidates.py | Network-free strict source-error and Telegram lookup tests. |
| tests/test_check_changed_files.py | Unit tests for the changed-file allowlist helper. |
| .github/workflows/discover.yml | 03:00 Warsaw selection, discovery orchestration, direct-main publication, and SHA summary. |
| .github/workflows/validate.yml | Run the new standard-library tests on push and pull request. |
| .catalog/README.md | Document the schedule, direct candidate-only publication, and no-API setup. |

### Task 1: Make strict discovery atomic

**Files:**

- Modify: .catalog/scripts/discover_candidates.py:398-468, 520-626
- Create: tests/test_discover_candidates.py

**Interfaces:**

- Consumes: HttpClient, repository_item, ADAPTERS, write_csv, and CANDIDATE_FIELDS.
- Produces: telegram_items(client, source, since, limit, fail_on_repository_error=False) and --fail-on-source-error.
- Guarantees: strict mode returns 1 and does not call write_csv after any source error.

- [ ] **Step 1: Write the failing tests**

Create tests/test_discover_candidates.py:

~~~python
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discover_candidates as discovery


class StrictDiscoveryTests(unittest.TestCase):
    def test_strict_source_error_returns_one_without_writing_candidates(self) -> None:
        source = {"Name": "Broken", "Provider": "Unsupported"}
        with (
            patch.object(sys, "argv", ["discover_candidates.py", "--write", "--fail-on-source-error"]),
            patch.object(discovery, "load_catalog", return_value=([], [])),
            patch.object(discovery, "load_candidates", return_value=(discovery.CANDIDATE_FIELDS, [])),
            patch.object(discovery, "load_sources", return_value=[source]),
            patch.object(discovery, "write_csv") as write_csv,
        ):
            self.assertEqual(discovery.main(), 1)
        write_csv.assert_not_called()

    def test_strict_telegram_lookup_error_is_propagated(self) -> None:
        class FakeClient:
            def get_text(self, url: str) -> str:
                return (
                    '<div class="tgme_widget_message_wrap" data-post="channel/1">'
                    '<time datetime="2026-08-25T00:00:00+00:00"></time>'
                    '<a href="https://github.com/example/tool">tool</a></div>'
                )

        source = {"Query": "https://t.me/s/channel"}
        with patch.object(discovery, "repository_item", side_effect=RuntimeError("timeout")):
            with self.assertRaisesRegex(RuntimeError, "Telegram repository lookup failed"):
                discovery.telegram_items(FakeClient(), source, "2026-08-25", 10, True)


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] **Step 2: Run the focused test to verify failure**

Run:

~~~bash
python3 -m unittest tests/test_discover_candidates.py -v
~~~

Expected: the parser rejects --fail-on-source-error, and telegram_items rejects its fifth positional argument.

- [ ] **Step 3: Implement strict source behavior**

Add this parser option after --report:

~~~python
parser.add_argument(
    "--fail-on-source-error",
    action="store_true",
    help="Return failure and leave candidates unchanged when any source lookup fails",
)
~~~

Change the Telegram adapter signature and exception branch:

~~~python
def telegram_items(
    client: HttpClient,
    source: dict[str, str],
    since: str,
    limit: int,
    fail_on_repository_error: bool = False,
) -> list[dict[str, Any]]:
~~~

~~~python
        except Exception as error:
            message = f"Telegram repository lookup failed: {repository_url}: {error}"
            if fail_on_repository_error:
                raise RuntimeError(message) from error
            print(message.replace("failed", "skipped"), file=sys.stderr)
            continue
~~~

Pass the keyword only to the Telegram adapter:

~~~python
        adapter_kwargs: dict[str, bool] = {}
        if source["Provider"] == "Telegram Channel":
            adapter_kwargs["fail_on_repository_error"] = args.fail_on_source_error
        try:
            items = adapter(client, source, since, args.max_per_source, **adapter_kwargs)
~~~

Generate the report before deciding whether to persist candidates. Before the existing write_csv call add:

~~~python
    if errors and args.fail_on_source_error:
        print(f"sources={len(sources)} new_candidates={len(new_rows)} errors={len(errors)}")
        return 1
~~~

This branch must run before write_csv. Preserve the current non-strict behavior for diagnostic runs.

- [ ] **Step 4: Run the focused gate**

~~~bash
python3 -m unittest tests/test_discover_candidates.py -v
python3 -m py_compile .catalog/scripts/discover_candidates.py
~~~

Expected: both tests pass and compilation succeeds.

- [ ] **Step 5: Commit Task 1**

~~~bash
git add .catalog/scripts/discover_candidates.py tests/test_discover_candidates.py
git commit -m "feat: fail strict candidate discovery on source errors"
~~~

### Task 2: Add a testable changed-file allowlist

**Files:**

- Create: .catalog/scripts/check_changed_files.py
- Create: tests/test_check_changed_files.py

**Interfaces:**

- Consumes: git diff --no-renames --name-only <base> and one or more --allow values.
- Produces: unexpected_paths(paths, allowed_paths) -> list[str].
- Guarantees: a direct nightly run fails when any tracked path except .catalog/data/candidates.csv changed.

- [ ] **Step 1: Write the failing helper tests**

Create tests/test_check_changed_files.py:

~~~python
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_changed_files


class ChangedFileTests(unittest.TestCase):
    def test_allows_only_candidate_csv(self) -> None:
        self.assertEqual(
            check_changed_files.unexpected_paths(
                [".catalog/data/candidates.csv"],
                [".catalog/data/candidates.csv"],
            ),
            [],
        )

    def test_reports_unique_sorted_disallowed_paths(self) -> None:
        self.assertEqual(
            check_changed_files.unexpected_paths(
                ["README.md", ".catalog/data/candidates.csv", "README.md", "AGENTIC.md"],
                [".catalog/data/candidates.csv"],
            ),
            ["AGENTIC.md", "README.md"],
        )


if __name__ == "__main__":
    unittest.main()
~~~

- [ ] **Step 2: Run the test to verify failure**

~~~bash
python3 -m unittest tests/test_check_changed_files.py -v
~~~

Expected: ModuleNotFoundError for check_changed_files.

- [ ] **Step 3: Implement the checker**

Create .catalog/scripts/check_changed_files.py:

~~~python
#!/usr/bin/env python3
"""Reject tracked working-tree paths outside an explicit allowlist."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Iterable


def unexpected_paths(paths: Iterable[str], allowed_paths: Iterable[str]) -> list[str]:
    allowed = set(allowed_paths)
    return sorted({path for path in paths if path and path not in allowed})


def changed_paths(base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--no-renames", "--name-only", base],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--allow", action="append", required=True)
    args = parser.parse_args()
    violations = unexpected_paths(changed_paths(args.base), args.allow)
    if not violations:
        return 0
    print("Unexpected tracked changes:", file=sys.stderr)
    print("\n".join(violations), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
~~~

- [ ] **Step 4: Run tests and the checker**

~~~bash
python3 -m unittest tests/test_check_changed_files.py -v
python3 .catalog/scripts/check_changed_files.py --base HEAD --allow .catalog/data/candidates.csv
~~~

Expected: tests pass and the checker exits 0 in a clean tree or a tree with only the allowed candidate CSV change.

- [ ] **Step 5: Commit Task 2**

~~~bash
git add .catalog/scripts/check_changed_files.py tests/test_check_changed_files.py
git commit -m "feat: guard nightly candidate staging"
~~~

### Task 3: Convert scheduled discovery to safe direct-main publication

**Files:**

- Modify: .github/workflows/discover.yml:1-88
- Modify: .github/workflows/validate.yml:18-26

**Interfaces:**

- Consumes: discover_candidates.py --write --fail-on-source-error, check_changed_files.py, GITHUB_TOKEN, and optional remote branch automation/catalog-candidates.
- Produces: one 03:00 Warsaw candidate discovery run, a candidate-only main commit, and a Git SHA in the job summary.
- Guarantees: no PR creation, no force push, no automatic candidate acceptance, and no push after a failure.

- [ ] **Step 1: Replace schedule and permissions**

Replace the trigger and permission blocks in discover.yml with:

~~~yaml
name: Discover and publish Awesome OSINT Repositories candidates

on:
  schedule:
    - cron: "0 1 * * *"
    - cron: "0 2 * * *"
  workflow_dispatch:

concurrency:
  group: catalogue-candidate-discovery
  cancel-in-progress: false

permissions:
  contents: write
~~~

Retain actions/checkout@v4 with fetch-depth: 0 and Python 3.12. Remove pull-requests: write and every gh pr command.

- [ ] **Step 2: Add schedule guard and legacy seed**

After Python setup, add:

~~~yaml
      - name: Decide whether to run
        id: schedule
        env:
          EVENT_NAME: ${{ github.event_name }}
        run: |
          if [ "$EVENT_NAME" = "workflow_dispatch" ] || [ "$(TZ=Europe/Warsaw date +%H)" = "03" ]; then
            echo "run=true" >> "$GITHUB_OUTPUT"
          else
            echo "run=false" >> "$GITHUB_OUTPUT"
            echo "Skipped: not 03:00 Europe/Warsaw." >> "$GITHUB_STEP_SUMMARY"
          fi

      - name: Fetch current main
        if: steps.schedule.outputs.run == 'true'
        run: |
          git fetch origin main
          git checkout --detach origin/main

      - name: Preserve legacy candidate queue
        if: steps.schedule.outputs.run == 'true'
        run: |
          branch="automation/catalog-candidates"
          if git ls-remote --exit-code origin "refs/heads/$branch" >/dev/null; then
            git fetch origin "+refs/heads/$branch:refs/remotes/origin/$branch"
            git show "refs/remotes/origin/$branch:.catalog/data/candidates.csv" > "$RUNNER_TEMP/previous-candidates.csv"
          fi
~~~

The legacy branch remains intact. Its candidate CSV is only a seed for the new direct-main queue.

- [ ] **Step 3: Add strict discovery, gates, and publication**

Add these steps after the seed, with the same schedule condition:

~~~yaml
      - name: Scan configured public sources
        if: steps.schedule.outputs.run == 'true'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          set -euo pipefail
          seed=()
          if [ -s "$RUNNER_TEMP/previous-candidates.csv" ]; then
            seed=(--seed-candidates "$RUNNER_TEMP/previous-candidates.csv")
          fi
          python .catalog/scripts/discover_candidates.py \
            --write \
            --fail-on-source-error \
            --lookback-days 14 \
            --max-per-source 100 \
            --delay 2.1 \
            "${seed[@]}" \
            --report "$RUNNER_TEMP/discovery-report.md"
          python -m py_compile .catalog/scripts/*.py
          python .catalog/scripts/render_catalog.py --check
          python .catalog/scripts/validate_catalog.py
          git diff --check
          python .catalog/scripts/check_changed_files.py \
            --base HEAD \
            --allow .catalog/data/candidates.csv

      - name: Commit and publish candidate queue
        if: steps.schedule.outputs.run == 'true'
        run: |
          set -euo pipefail
          if git diff --quiet -- .catalog/data/candidates.csv; then
            echo "No candidate queue change." >> "$GITHUB_STEP_SUMMARY"
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add .catalog/data/candidates.csv
          git diff --cached --quiet && exit 0
          git commit -m "chore: discover OSINT candidates"
          git fetch origin main
          git rebase origin/main
          python -m py_compile .catalog/scripts/*.py
          python .catalog/scripts/render_catalog.py --check
          python .catalog/scripts/validate_catalog.py
          git diff --check origin/main...HEAD
          git push origin HEAD:main
          local_sha=$(git rev-parse HEAD)
          remote_sha=$(git ls-remote origin refs/heads/main | awk 'NR == 1 { print $1 }')
          test "$local_sha" = "$remote_sha"
          {
            echo "## Nightly candidate discovery"
            echo
            echo "Commit: $local_sha"
            echo
            cat "$RUNNER_TEMP/discovery-report.md"
          } >> "$GITHUB_STEP_SUMMARY"
~~~

- [ ] **Step 4: Run tests from validation workflow**

Replace the validation run block with:

~~~yaml
        run: |
          python -m unittest discover -s tests -v
          python -m py_compile .catalog/scripts/*.py
          python .catalog/scripts/render_catalog.py --check
          python .catalog/scripts/validate_catalog.py
~~~

- [ ] **Step 5: Validate workflow syntax and commit Task 3**

~~~bash
if command -v actionlint >/dev/null; then actionlint .github/workflows/discover.yml .github/workflows/validate.yml; fi
git add .github/workflows/discover.yml .github/workflows/validate.yml
git commit -m "ci: publish nightly OSINT candidates"
~~~

Expected: no gh pr, git push --force, OPENAI_API_KEY, or pull-request write permission remains.

### Task 4: Document the candidate-only boundary

**Files:**

- Modify: .catalog/README.md:91-117, 169-175
- Modify: docs/superpowers/specs/2026-08-25-nightly-catalogue-autopublish-design.md

**Interfaces:**

- Consumes: Tasks 1 through 3.
- Produces: operator guidance that distinguishes autonomous discovery from human canonical acceptance.

- [ ] **Step 1: Add the strict command example**

Under the existing persisted-candidate command in .catalog/README.md, add:

~~~~markdown
The scheduled workflow uses strict mode. A failed source leaves the candidate
CSV unchanged and prevents publication:

~~~bash
GITHUB_TOKEN=github_token python3 .catalog/scripts/discover_candidates.py \
  --write \
  --fail-on-source-error \
  --lookback-days 14 \
  --report discovery-report.md
~~~
~~~~

- [ ] **Step 2: Replace scheduled-workflow guidance**

Change the discover.yml paragraph to state these exact rules:

- it runs once at 03:00 Europe/Warsaw using two UTC cron entries and a time guard;
- it merges the legacy candidate branch when present, scans configured sources, and commits only .catalog/data/candidates.csv directly to main after source, renderer, CSV, whitespace, and allowlist gates;
- each discovery remains Review Status: review, and review_candidate.py remains the only acceptance or rejection path;
- it requires no OpenAI key, personal token, or custom secret, only the repository-provided GITHUB_TOKEN with Actions write permission;
- it never force-pushes, closes the legacy PR, or performs a metadata refresh.

- [ ] **Step 3: Validate documentation**

~~~bash
python3 .catalog/scripts/render_catalog.py --check
python3 .catalog/scripts/validate_catalog.py
git diff --check
~~~

Expected: all commands pass. Do not run render_catalog.py --write, because documentation must not create generated-view changes.

- [ ] **Step 4: Commit documentation, accepted spec, and plan**

~~~bash
git add .catalog/README.md \
  docs/superpowers/specs/2026-08-25-nightly-catalogue-autopublish-design.md \
  docs/superpowers/plans/2026-08-25-nightly-candidate-discovery-without-api.md
git commit -m "docs: document nightly candidate discovery"
~~~

### Task 5: Verify, publish, and exercise the deployed workflow

**Files:**

- Verify: every path changed by Tasks 1 through 4.

**Interfaces:**

- Consumes: completed local commits on main, remote origin, and the repository's built-in Actions token.
- Produces: a clean branch matching origin/main and one manual workflow result.

- [ ] **Step 1: Run the full local gate**

~~~bash
python3 -m unittest discover -s tests -v
python3 -m py_compile .catalog/scripts/*.py
python3 .catalog/scripts/render_catalog.py --check
python3 .catalog/scripts/validate_catalog.py
git diff --check
git status --short
~~~

Expected: all checks pass and only intended committed work is present.

- [ ] **Step 2: Verify identity and publish**

~~~bash
git branch --show-current
git remote get-url origin
git log -4 --format='%h %an <%ae> %s'
git push origin main
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
~~~

Expected: branch main, remote https://github.com/oryon-osint/awesome-osint-repos.git, conventional commits without AI trailers, a non-force push, and equal local and remote-tracking SHAs.

- [ ] **Step 3: Trigger and watch one manual run**

~~~bash
gh workflow run discover.yml --repo oryon-osint/awesome-osint-repos --ref main
run_id=$(gh run list --repo oryon-osint/awesome-osint-repos --workflow discover.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$run_id" --repo oryon-osint/awesome-osint-repos
~~~

Expected: workflow_dispatch bypasses the time guard. It either completes with no candidate queue change or creates a normal candidate-only bot commit. A source error must fail without any push.

- [ ] **Step 4: Recheck final remote state**

~~~bash
git fetch origin main
git status --short
git rev-parse HEAD
git rev-parse origin/main
gh api repos/oryon-osint/awesome-osint-repos/commits/main --jq .sha
~~~

Expected: a clean tree and identical local, remote-tracking, and GitHub commit SHAs. Report the workflow-run URL, final SHA, and whether the first manual run published candidates or was a no-op.

## Self-Review

### Spec coverage

- 03:00 Warsaw and daylight-saving handling: Task 3, steps 1 and 2.
- No OpenAI API or custom secret: Tasks 3 and 4.
- Candidate-only direct publication: Tasks 2 and 3.
- No automatic acceptance or rejection: Tasks 3 and 4.
- Legacy queue preservation without deletion: Task 3, step 2.
- No partial source result: Tasks 1 and 3.
- Gates, safe rebase, non-force push, and SHA verification: Tasks 3 and 5.
- Weekly refresh stays separate: Task 4 does not modify refresh.yml.

### Completeness scan

The plan has no unresolved markers or vague implementation step. Every created function, CLI flag, test file, workflow block, validation command, and commit message is named above.

### Type consistency

- telegram_items consistently receives fail_on_repository_error: bool in Task 1, and only the Telegram adapter call supplies it.
- unexpected_paths(paths, allowed_paths) is defined in Task 2 and imported under the same name in its tests.
- The workflow calls the exact CLI names --fail-on-source-error, --base, and --allow defined in Tasks 1 and 2.
