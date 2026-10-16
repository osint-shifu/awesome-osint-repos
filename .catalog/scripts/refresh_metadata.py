#!/usr/bin/env python3
"""Refresh GitHub, GitLab, and Codeberg metadata and point-in-time snapshots."""

from __future__ import annotations

import argparse
import csv
from http.client import RemoteDisconnected
import json
import os
import re
import sys
import time
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from catalog_common import ALL_COLUMNS, DATA_ROOT, ROOT, is_iso_date, load_catalog, repository_identity, repository_key, write_csv_batch
from discover_candidates import HttpClient, gitlab_repository_status


SNAPSHOT_PATH = DATA_ROOT / "snapshots.csv"
CANDIDATE_PATH = DATA_ROOT / "candidates.csv"
GRAPHQL_BATCH_SIZE = 40
SNAPSHOT_FIELDS = [
    "Date", "Repository ID", "Repository", "Stars", "Forks", "Open Issues",
    "Last Update", "Archived",
]


class GitHubClient:
    def __init__(self, token: str = "", delay: float = 0.0) -> None:
        self.token = token
        self.delay = delay

    def get_json(
        self,
        url: str,
        missing_statuses: set[int] | None = None,
    ) -> tuple[int, dict[str, object] | None]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-osint-repos",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        for attempt in range(3):
            if self.delay:
                time.sleep(self.delay)
            try:
                with urlopen(Request(url, headers=headers), timeout=30) as response:
                    return response.status, json.load(response)
            except HTTPError as error:
                if error.code in (missing_statuses or {404}):
                    return error.code, None
                if error.code in {403, 429, 500, 502, 503, 504} and attempt < 2:
                    retry_after = int(error.headers.get("Retry-After", "0") or "0")
                    time.sleep(max(retry_after, 2 ** (attempt + 1)))
                    continue
                raise
            except (URLError, TimeoutError, RemoteDisconnected, ConnectionResetError) as error:
                if attempt == 2:
                    raise RuntimeError(str(error)) from error
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError(f"Unable to fetch {url}")

    def get_repository(self, owner: str, repository: str) -> tuple[int, dict[str, object] | None]:
        url = f"https://api.github.com/repos/{quote(owner)}/{quote(repository)}"
        return self.get_json(url)

    def get_default_branch_commit(
        self,
        owner: str,
        repository: str,
        branch: str,
    ) -> tuple[int, dict[str, object] | None]:
        url = (
            f"https://api.github.com/repos/{quote(owner)}/{quote(repository)}"
            f"/commits/{quote(branch, safe='')}"
        )
        return self.get_json(url, {404, 409, 422})

    def post_graphql(self, query: str) -> dict[str, object]:
        headers = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "awesome-osint-repos",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.token}",
        }
        body = json.dumps({"query": query}).encode()
        for attempt in range(3):
            if self.delay:
                time.sleep(self.delay)
            try:
                request = Request(
                    "https://api.github.com/graphql",
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urlopen(request, timeout=45) as response:
                    payload = json.load(response)
                if not isinstance(payload, dict):
                    raise RuntimeError("GitHub GraphQL returned an invalid response")
                errors = payload.get("errors") or []
                data = payload.get("data")
                fatal_errors = [
                    error
                    for error in errors
                    if not (
                        isinstance(error, dict)
                        and error.get("type") == "NOT_FOUND"
                        and isinstance(error.get("path"), list)
                        and re.fullmatch(r"r\d+", str(error["path"][0]))
                    )
                ]
                if fatal_errors or (errors and not isinstance(data, dict)):
                    raise RuntimeError(json.dumps(fatal_errors or errors, ensure_ascii=False))
                return payload
            except HTTPError as error:
                if error.code in {403, 429, 500, 502, 503, 504} and attempt < 2:
                    retry_after = int(error.headers.get("Retry-After", "0") or "0")
                    time.sleep(max(retry_after, 2 ** (attempt + 1)))
                    continue
                raise
            except (URLError, TimeoutError, RemoteDisconnected, ConnectionResetError) as error:
                if attempt == 2:
                    raise RuntimeError(str(error)) from error
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError("Unable to query GitHub GraphQL")

    def get_repositories_graphql(
        self,
        repositories: list[tuple[str, str]],
    ) -> list[dict[str, object] | None]:
        selections = []
        for index, (owner, repository) in enumerate(repositories):
            selections.append(
                f"""
                r{index}: repository(
                  owner: {json.dumps(owner)}
                  name: {json.dumps(repository)}
                ) {{
                  databaseId
                  url
                  createdAt
                  pushedAt
                  stargazerCount
                  isArchived
                  isFork
                  forkCount
                  issues(states: OPEN) {{ totalCount }}
                  licenseInfo {{ spdxId }}
                  defaultBranchRef {{
                    target {{
                      ... on Commit {{ committedDate }}
                    }}
                  }}
                }}
                """
            )
        payload = self.post_graphql("query {\n" + "\n".join(selections) + "\n}")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise RuntimeError("GitHub GraphQL response is missing data")

        results: list[dict[str, object] | None] = []
        for index in range(len(repositories)):
            repository = data.get(f"r{index}")
            if not isinstance(repository, dict):
                results.append(None)
                continue
            license_data = repository.get("licenseInfo") or {}
            issues_data = repository.get("issues") or {}
            default_branch = repository.get("defaultBranchRef") or {}
            target = default_branch.get("target") if isinstance(default_branch, dict) else {}
            results.append(
                {
                    "id": repository.get("databaseId"),
                    "html_url": repository.get("url"),
                    "created_at": repository.get("createdAt"),
                    "pushed_at": repository.get("pushedAt"),
                    "stargazers_count": repository.get("stargazerCount"),
                    "license": {
                        "spdx_id": (
                            license_data.get("spdxId")
                            if isinstance(license_data, dict)
                            else ""
                        )
                    },
                    "archived": repository.get("isArchived"),
                    "fork": repository.get("isFork"),
                    "forks_count": repository.get("forkCount"),
                    "open_issues_count": (
                        issues_data.get("totalCount")
                        if isinstance(issues_data, dict)
                        else 0
                    ),
                    "_default_branch_checked": True,
                    "_default_branch_committed_at": (
                        target.get("committedDate")
                        if isinstance(target, dict)
                        else ""
                    ),
                }
            )
        return results


def github_coordinates(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if parsed.netloc.casefold() != "github.com":
        return None
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    return parts[0], parts[1].removesuffix(".git")


def bool_text(value: object) -> str:
    return "true" if bool(value) else "false"


def public_repository_metadata(
    client: HttpClient, url: str,
) -> tuple[int, dict[str, object] | None]:
    parsed = urlparse(url)
    path = parsed.path.strip("/").removesuffix(".git")
    host = parsed.netloc.casefold()
    if host == "gitlab.com":
        endpoint = f"https://gitlab.com/api/v4/projects/{quote(path, safe='')}"
        hosting = "GitLab"
    elif host == "codeberg.org" and len(path.split("/")) == 2:
        owner, repository = path.split("/")
        endpoint = f"https://codeberg.org/api/v1/repos/{quote(owner)}/{quote(repository)}"
        hosting = "Codeberg"
    else:
        raise RuntimeError(f"Unsupported repository URL: {url}")
    try:
        metadata = client.get(endpoint)
    except HTTPError as error:
        if error.code == 404:
            return 404, None
        raise
    if not isinstance(metadata, dict):
        raise RuntimeError(f"{hosting} returned invalid repository metadata")
    if hosting == "GitLab":
        archived, fork = gitlab_repository_status(client, metadata, path)
    else:
        if not isinstance(metadata.get("archived"), bool) or not isinstance(metadata.get("fork"), bool):
            raise RuntimeError("Codeberg repository status could not be verified")
        archived, fork = metadata["archived"], metadata["fork"]
    branch = str(metadata.get("default_branch") or "")
    committed_at = ""
    if branch and not archived:
        if hosting == "GitLab":
            commits = client.get(
                f"https://gitlab.com/api/v4/projects/{metadata['id']}/repository/commits"
                f"?ref_name={quote(branch, safe='')}&per_page=1"
            )
            if isinstance(commits, list) and commits and isinstance(commits[0], dict):
                committed_at = str(commits[0].get("committed_date") or "")
        else:
            branch_data = client.get(f"{endpoint}/branches/{quote(branch, safe='')}")
            commit = branch_data.get("commit") if isinstance(branch_data, dict) else None
            if isinstance(commit, dict):
                committed_at = str(commit.get("timestamp") or "")
    normalized = {
        "id": metadata.get("id"),
        "html_url": metadata.get("web_url") if hosting == "GitLab" else metadata.get("html_url"),
        "hosting": hosting,
        "created_at": metadata.get("created_at"),
        "stargazers_count": metadata.get("star_count") if hosting == "GitLab" else metadata.get("stars_count"),
        "archived": archived, "fork": fork,
        "forks_count": metadata.get("forks_count"),
        "open_issues_count": metadata.get("open_issues_count"),
        "_default_branch_checked": True,
        "_default_branch_committed_at": committed_at,
    }
    if isinstance(metadata.get("license"), dict) and "spdx_id" in metadata["license"]:
        normalized["license"] = metadata["license"]
    return 200, normalized


def load_snapshots() -> list[dict[str, str]]:
    if not SNAPSHOT_PATH.exists():
        return []
    with SNAPSHOT_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def update_snapshot(rows: list[dict[str, str]], snapshot: dict[str, str]) -> None:
    key = (snapshot["Date"], repository_identity(snapshot))
    for index, row in enumerate(rows):
        existing = (row["Date"], repository_identity(row))
        if existing == key:
            rows[index] = snapshot
            return
    rows.append(snapshot)


def reconcile_candidates(
    catalogue: list[dict[str, str]],
    removed_keys: set[str],
    renamed_urls: dict[str, str] | None = None,
) -> tuple[list[str], list[dict[str, str]], int, int]:
    if not CANDIDATE_PATH.exists():
        return [], [], 0, 0
    with CANDIDATE_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        candidates = list(reader)

    canonical = {repository_key(row["Repository"]): row for row in catalogue}
    renamed_urls = renamed_urls or {}
    renamed_keys = {repository_key(url) for url in renamed_urls.values()}
    retained: list[dict[str, str]] = []
    changed_fields = 0
    removed = 0
    for candidate in candidates:
        key = repository_key(candidate["Repository"])
        if candidate.get("Review Status") == "accepted" and key in removed_keys:
            removed += 1
            continue
        if key in renamed_urls:
            candidate["Repository"] = renamed_urls[key]
            key = repository_key(candidate["Repository"])
            changed_fields += 1
        current = canonical.get(key)
        if candidate.get("Review Status") == "accepted" and current is not None:
            updates = {
                "Hosting": current["Hosting"],
                "Created": current["Created"],
                "Last Update": current["Last Update"],
                "Stars": current["Stars"],
                "License": current["License"],
                "Archived": current["Archived"],
                "Fork": current["Fork"],
            }
            for field, value in updates.items():
                if candidate.get(field, "") != value:
                    candidate[field] = value
                    changed_fields += 1
        retained.append(candidate)
    merged: list[dict[str, str]] = []
    by_key: dict[str, dict[str, str]] = {}
    priority = {"accepted": 2, "rejected": 1, "review": 0}
    for candidate in retained:
        key = repository_key(candidate["Repository"])
        previous = by_key.get(key) if key in renamed_keys else None
        if previous is None:
            merged.append(candidate)
            by_key[key] = candidate
            continue
        preferred, other = previous, candidate
        if priority.get(candidate.get("Review Status", ""), 0) > priority.get(previous.get("Review Status", ""), 0):
            preferred, other = candidate, previous
        combined = preferred.copy()
        for field in ("Notes", "Evidence", "Discovery Source", "Query"):
            combined[field] = "\n".join(dict.fromkeys(
                row[field] for row in (preferred, other) if row.get(field)
            ))
        previous.clear()
        previous.update(combined)
        removed += 1
    return fields, merged, changed_fields, removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write refreshed metadata")
    parser.add_argument("--snapshot", action="store_true", help="Append or update today's snapshot")
    parser.add_argument(
        "--drop-archived",
        action="store_true",
        help="Remove repositories confirmed as archived from the canonical catalogue",
    )
    parser.add_argument("--drop-unavailable", action="store_true", help="Remove repositories confirmed as unavailable")
    parser.add_argument(
        "--drop-stale-before",
        default="",
        help="Remove repositories whose latest default-branch commit predates YYYY-MM-DD",
    )
    parser.add_argument("--limit", type=int, default=0, help="Process at most this many repositories")
    parser.add_argument("--repository", action="append", default=[], help="Process only matching repository URL")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between API requests")
    args = parser.parse_args()

    fields, rows = load_catalog()
    if fields != ALL_COLUMNS:
        print("Canonical catalogue schema does not match ALL_COLUMNS", file=sys.stderr)
        return 2
    original_keys = {repository_key(row["Repository"]) for row in rows}

    requested = {repository_key(value) for value in args.repository}
    if (requested or args.limit) and (args.drop_archived or args.drop_unavailable or args.drop_stale_before):
        print(
            "Removal options require a full refresh "
            "without --repository or --limit",
            file=sys.stderr,
        )
        return 2
    selected = [
        row for row in rows
        if (not requested or repository_key(row["Repository"]) in requested)
    ]
    if args.limit:
        selected = selected[: args.limit]

    client = GitHubClient(os.environ.get("GITHUB_TOKEN", ""), args.delay)
    public_client = HttpClient(delay=args.delay)
    github_rows = [row for row in selected if github_coordinates(row["Repository"])]
    if len(github_rows) > 30 and not client.token:
        print(
            "GITHUB_TOKEN is required when refreshing more than 30 GitHub repositories",
            file=sys.stderr,
        )
        return 2
    snapshots = load_snapshots()
    today = date.today().isoformat()
    changed_fields = 0
    unavailable = 0
    removed_unavailable = 0
    removed_archived = 0
    removed_stale = 0
    removed_snapshots = 0
    removed_candidates = 0
    candidate_changed_fields = 0
    verified_last_update_keys: set[str] = set()
    renamed_urls: dict[str, str] = {}
    failures: list[str] = []

    if args.drop_stale_before and not is_iso_date(args.drop_stale_before):
        print("--drop-stale-before must use YYYY-MM-DD", file=sys.stderr)
        return 2

    graphql_metadata: dict[str, dict[str, object] | None] | None = None
    if client.token and github_rows:
        graphql_metadata = {}
        for start in range(0, len(github_rows), GRAPHQL_BATCH_SIZE):
            batch = github_rows[start : start + GRAPHQL_BATCH_SIZE]
            coordinates = [github_coordinates(row["Repository"]) for row in batch]
            assert all(value is not None for value in coordinates)
            try:
                metadata_batch = client.get_repositories_graphql(
                    [value for value in coordinates if value is not None]
                )
                graphql_metadata.update(zip((row["Repository"] for row in batch), metadata_batch))
            except Exception as error:
                failures.append(f"GitHub GraphQL batch {start // GRAPHQL_BATCH_SIZE + 1}: {error}")
                break
            print(
                f"[graphql {min(start + len(batch), len(github_rows))}/{len(github_rows)}] "
                "repository metadata"
            )

    if failures:
        print("Metadata refresh failed without writing partial results:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    for index, row in enumerate(selected, 1):
        coordinates = github_coordinates(row["Repository"])
        try:
            if coordinates is None:
                status, metadata = public_repository_metadata(public_client, row["Repository"])
            elif graphql_metadata is not None and graphql_metadata.get(row["Repository"]) is not None:
                metadata = graphql_metadata[row["Repository"]]
                status = 200
            else:
                assert coordinates is not None
                status, metadata = client.get_repository(*coordinates)
        except Exception as error:
            failures.append(f"{row['Repository']}: {error}")
            continue

        if status == 404:
            unavailable += 1
            if row.get("Repository Status") != "unavailable":
                row["Repository Status"] = "unavailable"
                changed_fields += 1
            row["Verified"] = today
            print(f"[{index}/{len(selected)}] unavailable {row['Repository']}")
            continue
        if not isinstance(metadata, dict):
            failures.append(f"{row['Repository']}: invalid repository metadata")
            continue
        if metadata.get("archived") is True and args.drop_archived:
            row["Archived"] = "true"
            row["Repository Status"] = "archived"
            print(f"[{index}/{len(selected)}] archived {row['Repository']}")
            continue

        license_data = metadata.get("license") or {}
        license_id = (
            license_data.get("spdx_id") if isinstance(license_data, dict) else ""
        ) if "license" in metadata else row.get("License", "")
        if license_id == "NOASSERTION":
            license_id = ""
        last_update = ""
        default_branch_commit = str(
            metadata.get("_default_branch_committed_at") or ""
        )[:10]
        if default_branch_commit:
            last_update = default_branch_commit
            verified_last_update_keys.add(repository_key(row["Repository"]))
        elif not metadata.get("_default_branch_checked"):
            assert coordinates is not None
            owner, repository = coordinates
            default_branch = str(metadata.get("default_branch") or "")
            branch_commit = None
            try:
                if default_branch:
                    _, branch_commit = client.get_default_branch_commit(
                        owner,
                        repository,
                        default_branch,
                    )
            except Exception as error:
                failures.append(f"{row['Repository']} default branch: {error}")
                continue
            if branch_commit is not None:
                commit_data = branch_commit.get("commit") or {}
                if isinstance(commit_data, dict):
                    committer_data = commit_data.get("committer") or {}
                    author_data = commit_data.get("author") or {}
                    if isinstance(committer_data, dict) and committer_data.get("date"):
                        last_update = str(committer_data["date"])[:10]
                        verified_last_update_keys.add(repository_key(row["Repository"]))
                    elif isinstance(author_data, dict) and author_data.get("date"):
                        last_update = str(author_data["date"])[:10]
                        verified_last_update_keys.add(repository_key(row["Repository"]))
        try:
            date.fromisoformat(last_update)
        except ValueError:
            failures.append(f"{row['Repository']}: default branch commit date could not be verified")
            continue
        canonical_url = str(metadata.get("html_url") or row["Repository"])
        if canonical_url != row["Repository"]:
            renamed_urls[repository_key(row["Repository"])] = canonical_url
        verified_last_update_keys.add(repository_key(canonical_url))
        archived = bool(metadata.get("archived"))
        updates = {
            "Repository": canonical_url,
            "Hosting": str(metadata.get("hosting") or "GitHub"),
            "Repository ID": str(metadata.get("id") or ""),
            "Created": str(metadata.get("created_at") or "")[:10],
            "Last Update": last_update,
            "Stars": str(metadata.get("stargazers_count") or 0),
            "License": str(license_id or ""),
            "Archived": bool_text(archived),
            "Fork": bool_text(metadata.get("fork")),
            "Repository Status": "archived" if archived else "active",
            "Verified": today,
        }
        for field, value in updates.items():
            if row.get(field, "") != value:
                row[field] = value
                changed_fields += 1

        if args.snapshot:
            update_snapshot(
                snapshots,
                {
                    "Date": today,
                    "Repository ID": str(metadata.get("id") or ""),
                    "Repository": canonical_url,
                    "Stars": str(metadata.get("stargazers_count") or 0),
                    "Forks": str(metadata["forks_count"]) if metadata.get("forks_count") is not None else "",
                    "Open Issues": str(metadata["open_issues_count"]) if metadata.get("open_issues_count") is not None else "",
                    "Last Update": last_update,
                    "Archived": bool_text(archived),
                },
            )
        print(f"[{index}/{len(selected)}] refreshed {canonical_url}")

    if failures:
        print("Metadata refresh failed without writing partial results:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    canonical = [repository_key(row["Repository"]) for row in rows]
    if len(canonical) != len(set(canonical)):
        print("Metadata refresh produced duplicate canonical URLs; no files were written", file=sys.stderr)
        return 1

    if args.drop_unavailable:
        retained_rows = [row for row in rows if row.get("Repository Status") != "unavailable"]
        removed_unavailable = len(rows) - len(retained_rows)
        rows = retained_rows

    if args.drop_archived:
        retained_rows = [row for row in rows if row.get("Archived") != "true"]
        removed_archived = len(rows) - len(retained_rows)
        rows = retained_rows

    if args.drop_stale_before:
        retained_rows = [
            row for row in rows
            if row.get("Last Update", "") >= args.drop_stale_before
            or (
                repository_key(row["Repository"]) not in verified_last_update_keys
            )
        ]
        removed_stale = len(rows) - len(retained_rows)
        rows = retained_rows

    retained_keys = {repository_key(row["Repository"]) for row in rows}
    removed_keys = {
        key for key in original_keys - retained_keys
        if repository_key(renamed_urls.get(key, key)) not in retained_keys
    }
    candidate_fields, candidates, candidate_changed_fields, removed_candidates = (
        reconcile_candidates(rows, removed_keys, renamed_urls)
    )

    if args.snapshot:
        canonical_ids = {
            repository_identity(row) for row in rows if row.get("Repository ID", "")
        }
        retained_snapshots = [
            snapshot
            for snapshot in snapshots
            if repository_key(snapshot["Repository"]) in retained_keys
            or (
                snapshot.get("Repository ID", "")
                and repository_identity(snapshot) in canonical_ids
            )
        ]
        removed_snapshots = len(snapshots) - len(retained_snapshots)
        snapshots = retained_snapshots

    if args.write:
        updates = [(ROOT / "osint-repositories.csv", ALL_COLUMNS, rows)]
        if candidate_fields:
            updates.append((CANDIDATE_PATH, candidate_fields, candidates))
        if args.snapshot:
            snapshots.sort(key=lambda row: (row["Date"], repository_key(row["Repository"])))
            updates.append((SNAPSHOT_PATH, SNAPSHOT_FIELDS, snapshots))
        try:
            write_csv_batch(updates)
        except OSError as error:
            print(f"Metadata refresh could not be saved: {error}", file=sys.stderr)
            return 1
    print(
        f"processed={len(selected)} changed_fields={changed_fields} "
        f"unavailable={unavailable} removed_unavailable={removed_unavailable} removed_archived={removed_archived} "
        f"removed_stale={removed_stale} "
        f"candidate_changed_fields={candidate_changed_fields} "
        f"removed_candidates={removed_candidates} "
        f"removed_snapshots={removed_snapshots} "
        f"mode={'write' if args.write else 'dry-run'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
