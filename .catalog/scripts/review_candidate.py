#!/usr/bin/env python3
"""Accept or reject one discovered candidate without editing CSV files by hand."""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import date
from urllib.parse import quote, urlparse

from catalog_common import (
    ALL_CATEGORIES,
    ALL_COLUMNS,
    MIN_LAST_UPDATE,
    ROOT,
    canonical_source_files,
    canonical_target_inputs,
    load_catalog,
    repository_key,
    split_values,
    write_csv,
)
from discover_candidates import CANDIDATE_FIELDS, CANDIDATE_PATH, HttpClient
from refresh_metadata import GitHubClient, bool_text, github_coordinates


def load_candidates() -> list[dict[str, str]]:
    with CANDIDATE_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def refresh_github_candidate(candidate: dict[str, str]) -> str:
    coordinates = github_coordinates(candidate["Repository"])
    if coordinates is None:
        return ""
    owner, repository = coordinates
    client = GitHubClient(os.environ.get("GITHUB_TOKEN", ""))
    status, metadata = client.get_repository(owner, repository)
    if status == 404 or metadata is None:
        raise RuntimeError("repository is unavailable")
    if metadata.get("archived"):
        candidate["Archived"] = "true"
        raise RuntimeError("repository is archived")

    default_branch = str(metadata.get("default_branch") or "")
    if not default_branch:
        raise RuntimeError("repository has no default branch")
    _, branch_commit = client.get_default_branch_commit(owner, repository, default_branch)
    if branch_commit is None:
        raise RuntimeError("default branch commit could not be verified")
    commit_data = branch_commit.get("commit") or {}
    committer_data = commit_data.get("committer") if isinstance(commit_data, dict) else {}
    author_data = commit_data.get("author") if isinstance(commit_data, dict) else {}
    committed_at = ""
    if isinstance(committer_data, dict):
        committed_at = str(committer_data.get("date") or "")
    if not committed_at and isinstance(author_data, dict):
        committed_at = str(author_data.get("date") or "")
    if not committed_at:
        raise RuntimeError("default branch commit date could not be verified")

    license_data = metadata.get("license") or {}
    license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else ""
    if license_id == "NOASSERTION":
        license_id = ""
    candidate.update(
        {
            "Repository": str(metadata.get("html_url") or candidate["Repository"]),
            "Hosting": "GitHub",
            "Created": str(metadata.get("created_at") or "")[:10],
            "Last Update": committed_at[:10],
            "Stars": str(metadata.get("stargazers_count") or 0),
            "Language": str(metadata.get("language") or candidate.get("Language") or ""),
            "License": str(license_id or ""),
            "Archived": "false",
            "Fork": bool_text(metadata.get("fork")),
        }
    )
    return str(metadata.get("id") or "")


def refresh_gitlab_candidate(candidate: dict[str, str]) -> str:
    parsed = urlparse(candidate["Repository"])
    project_path = parsed.path.strip("/")
    if parsed.netloc.casefold() != "gitlab.com" or not project_path:
        raise RuntimeError("invalid GitLab repository URL")
    client = HttpClient()
    metadata = client.get(
        f"https://gitlab.com/api/v4/projects/{quote(project_path, safe='')}"
    )
    if not isinstance(metadata, dict):
        raise RuntimeError("GitLab returned invalid repository metadata")
    if metadata.get("archived"):
        raise RuntimeError("repository is archived")
    default_branch = str(metadata.get("default_branch") or "")
    if not default_branch:
        raise RuntimeError("repository has no default branch")
    commits = client.get(
        f"https://gitlab.com/api/v4/projects/{metadata['id']}/repository/commits"
        f"?ref_name={quote(default_branch, safe='')}&per_page=1"
    )
    if not isinstance(commits, list) or not commits:
        raise RuntimeError("default branch commit could not be verified")
    committed_at = str(commits[0].get("committed_date") or "")
    if not committed_at:
        raise RuntimeError("default branch commit date could not be verified")
    candidate.update(
        {
            "Repository": str(metadata.get("web_url") or candidate["Repository"]),
            "Hosting": "GitLab",
            "Created": str(metadata.get("created_at") or "")[:10],
            "Last Update": committed_at[:10],
            "Stars": str(metadata.get("star_count") or 0),
            "Archived": "false",
            "Fork": bool_text(metadata.get("forked_from_project")),
        }
    )
    return str(metadata.get("id") or "")


def refresh_codeberg_candidate(candidate: dict[str, str]) -> str:
    parsed = urlparse(candidate["Repository"])
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if parsed.netloc.casefold() != "codeberg.org" or len(parts) < 2:
        raise RuntimeError("invalid Codeberg repository URL")
    owner, repository = parts[:2]
    client = HttpClient()
    metadata = client.get(
        f"https://codeberg.org/api/v1/repos/{quote(owner)}/{quote(repository)}"
    )
    if not isinstance(metadata, dict):
        raise RuntimeError("Codeberg returned invalid repository metadata")
    if metadata.get("archived"):
        raise RuntimeError("repository is archived")
    default_branch = str(metadata.get("default_branch") or "")
    if not default_branch:
        raise RuntimeError("repository has no default branch")
    branch = client.get(
        f"https://codeberg.org/api/v1/repos/{quote(owner)}/{quote(repository)}"
        f"/branches/{quote(default_branch, safe='')}"
    )
    commit = branch.get("commit") if isinstance(branch, dict) else {}
    committed_at = str(commit.get("timestamp") or "") if isinstance(commit, dict) else ""
    if not committed_at:
        raise RuntimeError("default branch commit date could not be verified")
    candidate.update(
        {
            "Repository": str(metadata.get("html_url") or candidate["Repository"]),
            "Hosting": "Codeberg",
            "Created": str(metadata.get("created_at") or "")[:10],
            "Last Update": committed_at[:10],
            "Stars": str(metadata.get("stars_count") or 0),
            "Language": str(metadata.get("language") or candidate.get("Language") or ""),
            "Archived": "false",
            "Fork": bool_text(metadata.get("fork")),
        }
    )
    return str(metadata.get("id") or "")


def refresh_candidate_metadata(candidate: dict[str, str]) -> str:
    host = urlparse(candidate["Repository"]).netloc.casefold()
    if host == "github.com":
        return refresh_github_candidate(candidate)
    if host == "gitlab.com":
        return refresh_gitlab_candidate(candidate)
    if host == "codeberg.org":
        return refresh_codeberg_candidate(candidate)
    raise RuntimeError(f"unsupported repository host: {host or 'missing'}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", help="Candidate repository URL")
    decision = parser.add_mutually_exclusive_group(required=True)
    decision.add_argument("--accept", action="store_true")
    decision.add_argument("--reject", action="store_true")
    parser.add_argument("--project", help="Override project name")
    parser.add_argument(
        "--target-input",
        default="",
        help="Concrete input type; separate multiple values with semicolons",
    )
    parser.add_argument("--category", help="One main catalogue category")
    parser.add_argument(
        "--view",
        action="append",
        default=[],
        help="Additional generated view: EMERGING.md or AGENTIC.md; may be repeated",
    )
    parser.add_argument("--type", dest="project_type", help="Language or integration type")
    parser.add_argument("--ai-agent", default="", help="Documented agent runtime or compatibility")
    parser.add_argument("--description", help="Curated neutral description")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    candidates = load_candidates()
    key = repository_key(args.repository)
    candidate = next((row for row in candidates if repository_key(row["Repository"]) == key), None)
    if candidate is None:
        print(f"Candidate not found: {args.repository}", file=sys.stderr)
        return 1

    if args.reject:
        candidate["Review Status"] = "rejected"
        candidate["Notes"] = args.notes
        write_csv(CANDIDATE_PATH, CANDIDATE_FIELDS, candidates)
        print(f"rejected {candidate['Repository']}")
        return 0

    repository_id = ""
    try:
        repository_id = refresh_candidate_metadata(candidate)
    except Exception as error:
        print(
            f"Candidate metadata verification failed: {candidate['Repository']}: {error}",
            file=sys.stderr,
        )
        return 1
    key = repository_key(candidate["Repository"])

    if candidate.get("Archived") == "true":
        print(
            f"Archived repositories cannot be accepted: {candidate['Repository']}",
            file=sys.stderr,
        )
        return 1

    if candidate.get("Last Update", "") < MIN_LAST_UPDATE:
        print(
            f"Repositories inactive since before {MIN_LAST_UPDATE} cannot be accepted: "
            f"{candidate['Repository']}",
            file=sys.stderr,
        )
        return 1

    required = {
        "category": args.category,
        "type": args.project_type,
        "description": args.description,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print(f"Acceptance requires: {', '.join('--' + name for name in missing)}", file=sys.stderr)
        return 2

    fields, catalogue = load_catalog()
    if fields != ALL_COLUMNS:
        print("Canonical catalogue schema does not match ALL_COLUMNS", file=sys.stderr)
        return 1
    if any(repository_key(row["Repository"]) == key for row in catalogue):
        print(f"Repository is already catalogued: {candidate['Repository']}", file=sys.stderr)
        return 1

    try:
        final_targets = canonical_target_inputs(args.target_input)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.category not in ALL_CATEGORIES:
        print(f"Unknown category: {args.category}", file=sys.stderr)
        return 2
    requested_views: list[str] = []
    for value in args.view:
        requested_views.extend(split_values(value))
    try:
        source_files = canonical_source_files(["README.md", *requested_views])
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    if "AGENTIC.md" in source_files and not args.ai_agent.strip():
        print("--ai-agent is required for AGENTIC.md entries", file=sys.stderr)
        return 2

    catalogue.append(
        {
            "Project": args.project or candidate["Project"],
            "Repository": candidate["Repository"],
            "Description": args.description or candidate["Description"],
            "Target Input": "; ".join(final_targets),
            "Categories": args.category,
            "Type": args.project_type or candidate["Language"] or "Unknown",
            "AI Agent": args.ai_agent,
            "License": candidate["License"],
            "Stars": candidate["Stars"] or "0",
            "Created": candidate["Created"],
            "Last Update": candidate["Last Update"],
            "Added": date.today().isoformat(),
            "Verified": date.today().isoformat(),
            "Hosting": candidate["Hosting"],
            "Repository ID": repository_id,
            "Archived": candidate["Archived"],
            "Fork": candidate["Fork"],
            "Repository Status": "archived" if candidate["Archived"] == "true" else "active",
            "Review Status": "accepted",
            "Discovery Source": candidate["Discovery Source"],
            "Source Files": "; ".join(source_files),
        }
    )
    candidate["Review Status"] = "accepted"
    candidate["Notes"] = args.notes
    write_csv(ROOT / "osint-repositories.csv", ALL_COLUMNS, catalogue)
    write_csv(CANDIDATE_PATH, CANDIDATE_FIELDS, candidates)
    print(f"accepted {candidate['Repository']}; run render_catalog.py --write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
