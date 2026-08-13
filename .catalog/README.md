<a id="top"></a>

<div align="center">
  <h1>Awesome OSINT Repositories Monitoring</h1>
  <p>Automation and review guide for maintaining a verified catalogue of open-source OSINT tools and the public source-code repositories that contain their implementations.</p>
  <p>
    <img alt="Publication policy: review gated" src="https://img.shields.io/badge/publication-review_gated-bf8700?style=flat-square">
    <img alt="Metadata refresh: weekly" src="https://img.shields.io/badge/metadata-weekly-0969da?style=flat-square">
    <img alt="Candidate discovery: daily" src="https://img.shields.io/badge/discovery-daily-8250df?style=flat-square">
    <img alt="Third-party code execution: disabled" src="https://img.shields.io/badge/third--party_code-not_executed-1f883d?style=flat-square">
    <img alt="Last update: 2026-08-13" src="https://img.shields.io/badge/last_update-2026--08--13-1f883d?style=flat-square">
  </p>
  <p><strong><a href="README.md">Monitoring</a></strong> · <a href="../README.md">Awesome OSINT Repositories</a> · <a href="../EMERGING.md">Emerging Projects</a> · <a href="../AGENTIC.md">Agentic AI OSINT</a> · <a href="../TIMELINE.md">Catalogue Timeline</a> · <a href="../osint-repositories.csv">Repository Database CSV</a></p>
</div>

## Operating model

`../osint-repositories.csv` is the canonical, deduplicated repository database in CSV format. The Markdown tables are generated views of accepted open-source tool and integration records. Candidate discovery is intentionally separate from publication.

The canonical CSV stores the publication date in its `Added` column. The renderer places a 6 px green dot before projects in public Markdown views for 14 days after acceptance.

`Categories` stores exactly one of the 12 main catalogue categories. `Target Input` stores only concrete data accepted or investigated by a tool and may contain several semicolon-separated values. `AI Agent` records documented agent compatibility. Membership in the additional `EMERGING.md` and `AGENTIC.md` views is stored separately in `Source Files`.

```text
.catalog/data/sources.csv -> discover_candidates.py -> .catalog/data/candidates.csv -> human review
                                                                           -> osint-repositories.csv
GitHub API -> refresh_metadata.py -> osint-repositories.csv + .catalog/data/snapshots.csv
osint-repositories.csv -> render_catalog.py -> README.md + EMERGING.md + AGENTIC.md + TIMELINE.md
all catalogue files -> validate_catalog.py -> pass or fail
```

The monitor never clones, imports, installs, or executes code from catalogued repositories. It reads public repository metadata and registry records only.

## Files

| File | Purpose |
|---|---|
| `../osint-repositories.csv` | Canonical CSV database of accepted open-source tool records, publication dates, and current repository metadata. |
| `data/candidates.csv` | Automatically discovered repositories with a suggested target input, main category, and optional generated views, awaiting an explicit decision. |
| `data/sources.csv` | Enabled discovery queries, providers, windows, suggested target inputs, categories, and optional generated views. |
| `data/snapshots.csv` | Point-in-time metadata used for trend and change reporting. |
| `../README.md` | Generated main catalogue organized into 12 mutually exclusive categories. |
| `../EMERGING.md` | Generated early-stage project view. |
| `../AGENTIC.md` | Generated skills, plugins, MCP, and agent integration views. |
| `../TIMELINE.md` | Generated visual chronology of additions with descriptions, categories, and current star counts. |

## Canonical taxonomy

Every accepted record has exactly one main category:

`Identity`, `Social Media`, `Code Repositories`, `Infrastructure`, `Web`, `Dark Web`, `Threat Intelligence`, `Documents & Records`, `Media`, `Geolocation`, `Cryptocurrency`, or `Investigation`.

Allowed `Target Input` values are:

`Name`, `Username`, `Email`, `Phone Number`, `Domain`, `IP Address`, `ASN`, `CIDR`, `URL`, `Onion Service`, `Image`, `Location`, `BSSID / SSID`, `Organization Name`, `Crypto Address`, `File Hash`, `Document`, `Keyword`, `Video`, `Repository URL`, `Event Data`, `Coordinates`, `Dataset`, `CVE ID`, `File`, `Audio`, `Text`, and `Aircraft ID`.

`Target Input` may contain several semicolon-separated values. It may be blank only when a tool has no fixed input type, such as a general investigation workspace or reusable agent workflow.

## Local commands

The scripts use the Python standard library and require Python 3.11 or newer.

Validate the canonical data and every generated table:

```bash
python3 -m py_compile .catalog/scripts/*.py
python3 .catalog/scripts/render_catalog.py --check
python3 .catalog/scripts/validate_catalog.py
```

Refresh GitHub metadata and save a daily snapshot. A token is required for the batched full-catalogue query:

```bash
GITHUB_TOKEN=github_token python3 .catalog/scripts/refresh_metadata.py \
  --write \
  --snapshot \
  --drop-archived \
  --drop-stale-before 2020-01-01 \
  --delay 0.1
python3 .catalog/scripts/render_catalog.py --write
python3 .catalog/scripts/validate_catalog.py
```

Run discovery against all enabled providers without changing files:

```bash
GITHUB_TOKEN=github_token python3 .catalog/scripts/discover_candidates.py --lookback-days 14 --report discovery-report.md
```

Limit a diagnostic run to one configured source with `--source "GitHub OSINT topic"`, or repeat `--provider` to select one or more providers.

Persist newly found candidates:

```bash
GITHUB_TOKEN=github_token python3 .catalog/scripts/discover_candidates.py --write --lookback-days 14 --report discovery-report.md
```

Run a one-off historical scan of the Cyber Detective public channel:

```bash
GITHUB_TOKEN=github_token python3 .catalog/scripts/discover_candidates.py \
  --write \
  --source "Cyber Detective Telegram" \
  --since 2026-01-01 \
  --max-per-source 1000 \
  --report cyber-detective-backfill.md
```

Generate a market-watch summary from candidates and snapshots:

```bash
python3 .catalog/scripts/market_report.py --output market-watch.md
```

Reports are operational artifacts and are not committed by the scheduled workflows.

## Candidate review

Automated discovery provides suggestions, not final classifications. Before accepting a repository, verify that it:

- contains meaningful, publicly accessible source code;
- has a practical OSINT, SOCMINT, GEOINT, recon, CTI, research, or evidence-analysis use case;
- is not merely a link collection, product landing page, prompt stub, exact repository duplicate, or canonical mirror;
- has a neutral description supported by its implementation and documentation;
- is assigned one appropriate main category;
- lists only concrete input types in `Target Input`, leaving it blank when no fixed input exists;
- documents any value stored in `AI Agent`;
- has a meaningful latest commit on its default branch rather than activity limited to abandoned side branches.

Functional overlap with another accepted project is not a rejection reason. Competing implementations remain useful for market coverage when each repository has a distinct, maintained implementation. Fork status alone is also not a rejection reason when the fork is the maintained implementation or an active successor.

Do not remove a project solely because one optional entry point or installation path fails. Check its documented primary workflow, current platform dependencies, and confirmed operational use before replacing it.

Reject a candidate:

```bash
python3 .catalog/scripts/review_candidate.py https://github.com/owner/repository --reject --notes "Not an implementation-bearing OSINT project"
```

Accept a standalone project:

```bash
python3 .catalog/scripts/review_candidate.py https://github.com/owner/repository \
  --accept \
  --target-input Domain \
  --category Infrastructure \
  --type Python \
  --description "Discovers public infrastructure associated with a domain."
python3 .catalog/scripts/render_catalog.py --write
python3 .catalog/scripts/validate_catalog.py
```

Use only values from the canonical `Target Input` taxonomy and assign exactly one `--category`. Add `--view EMERGING.md` for the watchlist. For an agent integration, add `--view AGENTIC.md` together with a documented `--ai-agent` value. Repeat `--view` when both generated views apply.

## Discovery sources

`.catalog/data/sources.csv` currently supports these adapters:

| Provider | Coverage | Authentication |
|---|---|---|
| GitHub Search | Topics and targeted repository queries | `GITHUB_TOKEN` recommended |
| GitLab Projects API | Public OSINT and recon project search | None for public results |
| Codeberg API | Public repository search | None for public results |
| Official MCP Registry | OSINT, recon, and research server search | None for public results |
| Cyber Detective Telegram | Direct GitHub, GitLab, and Codeberg links shared in public channel posts | None for public posts |

Edit `.catalog/data/sources.csv` to add, disable, or narrow a query. A new provider requires a corresponding adapter in `.catalog/scripts/discover_candidates.py`. Telegram channel adapters treat posts as leads and only send direct public repository links to manual review. Keep queries focused enough to make manual review practical.

## Scheduled workflows

- `validate.yml` checks Python syntax, generated Markdown drift, CSV integrity, links between local files, duplicate repositories, table schemas, the 12-category taxonomy, and allowed target inputs on every push and pull request.
- `refresh.yml` runs weekly, refreshes GitHub metadata, appends a snapshot, regenerates all catalogue tables, opens or updates a review pull request, and creates a dated market-watch issue.
- `discover.yml` runs daily, scans configured sources, and opens or updates a review pull request when `.catalog/data/candidates.csv` changes.

Scheduled workflows use the repository-provided `GITHUB_TOKEN`. The repository must allow GitHub Actions to create pull requests and grant workflows read and write permissions under **Settings -> Actions -> General**. GitHub may disable scheduled workflows in inactive public repositories, so the manual `workflow_dispatch` trigger remains available.

## Metadata and lifecycle policy

- `Last Update` records the date of the latest commit on the repository's default branch for GitHub records. Other hosts use the most precise repository activity date exposed by their API and are checked during review.
- `Stars` records an exact point-in-time value, never an approximation.
- `Verified` records the last successful metadata check.
- Renamed or transferred GitHub repositories are replaced with the canonical API URL.
- Repositories confirmed as archived are removed from the canonical catalogue and active monitoring data. GitHub status is enforced by the scheduled metadata refresh; other hosts are checked during review.
- Repository age is not a removal criterion. Repositories whose latest default-branch commit predates `2020-01-01` are removed, while older projects with current maintenance remain eligible.
- A recent push does not by itself prove operational usefulness. Stale integrations are reviewed for deprecated APIs, unsupported runtimes, broken installation paths, explicit maintenance notices, and maintained successors.
- A confirmed `404` marks a repository as unavailable. Transient network and API failures do not change repository status.
- Descriptions, target inputs, categories, source-file memberships, types, and AI-agent labels are never overwritten by metadata refreshes.

## Recommended review rhythm

| Frequency | Review |
|---|---|
| Daily | Triage new high-confidence candidates and obvious false positives. |
| Weekly | Review metadata pull request, star movement, archival changes, and unavailable repositories. |
| Monthly | Audit low-activity projects, category balance, target-input quality, source quality, and repeated discovery noise. |
| Quarterly | Revisit inclusion rules, providers, the 12-category taxonomy, allowed target inputs, and AI-agent labels. |

<p align="right"><a href="#top">Back to top ↑</a></p>
