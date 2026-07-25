#!/usr/bin/env python3
"""Discover repository candidates from configured public hosting and MCP sources."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

from catalog_common import (
    DATA_ROOT,
    MIN_LAST_UPDATE,
    load_catalog,
    repository_key,
    write_csv,
)


CANDIDATE_PATH = DATA_ROOT / "candidates.csv"
SOURCE_PATH = DATA_ROOT / "sources.csv"
CANDIDATE_FIELDS = [
    "Project", "Repository", "Hosting", "Discovered", "Discovery Source", "Query",
    "Suggested Target Input", "Suggested Category", "Suggested Views", "Description", "Created", "Last Update",
    "Stars", "Language", "License", "Archived", "Fork", "Score", "Confidence",
    "Evidence", "Review Status", "Notes",
]

RELEVANCE_TERMS = {
    "osint", "socmint", "geoint", "recon", "reconnaissance", "intelligence",
    "investigation", "forensics", "threat-intelligence", "username", "geolocation",
}


class HttpClient:
    def __init__(self, github_token: str = "", delay: float = 0.0) -> None:
        self.github_token = github_token
        self.delay = delay

    def get(self, url: str, github: bool = False) -> Any:
        headers = {"User-Agent": "awesome-osint-tools", "Accept": "application/json"}
        if github:
            headers.update({"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
            if self.github_token:
                headers["Authorization"] = f"Bearer {self.github_token}"
        for attempt in range(3):
            if self.delay:
                time.sleep(self.delay)
            try:
                with urlopen(Request(url, headers=headers), timeout=45) as response:
                    return json.load(response)
            except HTTPError as error:
                if error.code in {403, 429, 500, 502, 503, 504} and attempt < 2:
                    retry_after = int(error.headers.get("Retry-After", "0") or "0")
                    time.sleep(max(retry_after, 2 ** (attempt + 1)))
                    continue
                raise
            except (URLError, TimeoutError) as error:
                if attempt == 2:
                    raise RuntimeError(str(error)) from error
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError(f"Unable to fetch {url}")

    def get_text(self, url: str) -> str:
        headers = {
            "User-Agent": "awesome-osint-tools",
            "Accept": "text/html,application/xhtml+xml",
        }
        for attempt in range(3):
            if self.delay:
                time.sleep(self.delay)
            try:
                with urlopen(Request(url, headers=headers), timeout=45) as response:
                    return response.read().decode("utf-8", errors="replace")
            except HTTPError as error:
                if error.code in {403, 429, 500, 502, 503, 504} and attempt < 2:
                    retry_after = int(error.headers.get("Retry-After", "0") or "0")
                    time.sleep(max(retry_after, 2 ** (attempt + 1)))
                    continue
                raise
            except (URLError, TimeoutError) as error:
                if attempt == 2:
                    raise RuntimeError(str(error)) from error
                time.sleep(2 ** (attempt + 1))
        raise RuntimeError(f"Unable to fetch {url}")


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def iso_date(value: object) -> str:
    text = str(value or "")
    return text[:10] if re.match(r"\d{4}-\d{2}-\d{2}", text) else ""


def lifecycle_dates(item: dict[str, Any]) -> tuple[str, str] | None:
    created = iso_date(item.get("created"))
    updated = iso_date(item.get("updated"))
    if not created or not updated or updated < MIN_LAST_UPDATE:
        return None
    return created, updated


def bool_text(value: object) -> str:
    return "true" if bool(value) else "false"


def candidate_score(item: dict[str, Any]) -> int:
    text = " ".join(
        [clean_text(item.get("name")), clean_text(item.get("description")), " ".join(item.get("topics") or [])]
    ).casefold()
    topics = {str(topic).casefold() for topic in item.get("topics") or []}
    score = 0
    if "osint" in topics or "open-source-intelligence" in topics:
        score += 4
    score += min(3, sum(1 for term in RELEVANCE_TERMS if term in text))
    if item.get("language"):
        score += 1
    if int(item.get("size") or 0) >= 20:
        score += 1
    if item.get("license"):
        score += 1
    if int(item.get("stars") or 0) > 0:
        score += 1
    if item.get("archived"):
        score -= 5
    return score


def confidence(score: int) -> str:
    if score >= 8:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


def github_items(client: HttpClient, source: dict[str, str], since: str, limit: int) -> list[dict[str, Any]]:
    query = source["Query"]
    window = source["Window"]
    if window in {"created", "pushed"}:
        query += f" {window}:>={since}"
    query += " archived:false"
    params = urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": limit})
    payload = client.get(f"https://api.github.com/search/repositories?{params}", github=True)
    results = []
    for item in payload.get("items", []):
        license_data = item.get("license") or {}
        license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else ""
        if license_id == "NOASSERTION":
            license_id = ""
        results.append(
            {
                "name": item.get("name"),
                "url": item.get("html_url"),
                "hosting": "GitHub",
                "description": item.get("description"),
                "created": item.get("created_at"),
                "updated": item.get("pushed_at"),
                "stars": item.get("stargazers_count"),
                "language": item.get("language"),
                "license": license_id,
                "archived": item.get("archived"),
                "fork": item.get("fork"),
                "topics": item.get("topics") or [],
                "size": item.get("size") or 0,
            }
        )
    return results


def gitlab_items(client: HttpClient, source: dict[str, str], since: str, limit: int) -> list[dict[str, Any]]:
    params = urlencode(
        {
            "search": source["Query"], "visibility": "public", "active": "true",
            "last_activity_after": f"{since}T00:00:00Z", "order_by": "last_activity_at",
            "sort": "desc", "per_page": limit,
        }
    )
    payload = client.get(f"https://gitlab.com/api/v4/projects?{params}")
    return [
        {
            "name": item.get("name"), "url": item.get("web_url"), "hosting": "GitLab",
            "description": item.get("description"), "created": item.get("created_at"),
            "updated": item.get("last_activity_at"), "stars": item.get("star_count"),
            "language": "", "license": "", "archived": item.get("archived"),
            "fork": bool(item.get("forked_from_project")), "topics": item.get("topics") or [],
            "size": 0,
        }
        for item in payload
    ]


def codeberg_items(client: HttpClient, source: dict[str, str], since: str, limit: int) -> list[dict[str, Any]]:
    params = urlencode({"q": source["Query"], "limit": min(limit, 50), "sort": "updated", "order": "desc"})
    payload = client.get(f"https://codeberg.org/api/v1/repos/search?{params}")
    results = []
    for item in payload.get("data", []):
        if iso_date(item.get("created_at")) < since and source["Window"] == "created":
            continue
        results.append(
            {
                "name": item.get("name"), "url": item.get("html_url"), "hosting": "Codeberg",
                "description": item.get("description"), "created": item.get("created_at"),
                "updated": item.get("updated_at"), "stars": item.get("stars_count"),
                "language": item.get("language"), "license": "", "archived": item.get("archived"),
                "fork": item.get("fork"), "topics": item.get("topics") or [], "size": item.get("size") or 0,
            }
        )
    return results


def find_repository_url(value: object) -> str:
    if isinstance(value, str) and re.match(r"https://(?:github\.com|gitlab\.com|codeberg\.org)/[^/]+/[^/]+", value):
        return value.split("#", 1)[0].removesuffix(".git")
    if isinstance(value, dict):
        for key in ("repository", "url", "source", "homepage"):
            if key in value:
                found = find_repository_url(value[key])
                if found:
                    return found
        for nested in value.values():
            found = find_repository_url(nested)
            if found:
                return found
    if isinstance(value, list):
        for nested in value:
            found = find_repository_url(nested)
            if found:
                return found
    return ""


def mcp_items(client: HttpClient, source: dict[str, str], since: str, limit: int) -> list[dict[str, Any]]:
    params = urlencode({"search": source["Query"], "limit": min(limit, 100), "updated_since": f"{since}T00:00:00.000Z"})
    payload = client.get(f"https://registry.modelcontextprotocol.io/v0.1/servers?{params}")
    results = []
    for entry in payload.get("servers", []):
        server = entry.get("server", entry)
        url = find_repository_url(server)
        if not url:
            continue
        results.append(
            {
                "name": server.get("name") or url.rstrip("/").rsplit("/", 1)[-1],
                "url": url, "hosting": urlparse(url).netloc, "description": server.get("description"),
                "created": entry.get("publishedAt") or entry.get("createdAt"),
                "updated": entry.get("updatedAt") or entry.get("publishedAt"),
                "stars": 0, "language": "", "license": "", "archived": False,
                "fork": False, "topics": ["mcp"], "size": 1,
            }
        )
    return results


def normalize_repository_url(value: str) -> str:
    parsed = urlparse(unescape(value.strip()))
    host = parsed.netloc.casefold().removeprefix("www.")
    parts = [part for part in parsed.path.split("/") if part]
    if host == "github.com":
        if len(parts) < 2 or parts[0].casefold() in {
            "features", "marketplace", "orgs", "search", "sponsors", "topics", "users",
        }:
            return ""
        parts = parts[:2]
    elif host == "codeberg.org":
        if len(parts) < 2:
            return ""
        parts = parts[:2]
    elif host == "gitlab.com":
        if "-" in parts:
            parts = parts[:parts.index("-")]
        if len(parts) < 2:
            return ""
    else:
        return ""
    parts[-1] = parts[-1].removesuffix(".git")
    return f"https://{host}/{'/'.join(parts)}"


def repository_item(client: HttpClient, repository_url: str, evidence: str) -> dict[str, Any] | None:
    parsed = urlparse(repository_url)
    parts = [part for part in parsed.path.split("/") if part]
    host = parsed.netloc.casefold()
    if host == "github.com":
        owner, repository = parts[:2]
        metadata = client.get(
            f"https://api.github.com/repos/{quote(owner)}/{quote(repository)}",
            github=True,
        )
        if metadata.get("archived"):
            return None
        license_data = metadata.get("license") or {}
        license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else ""
        if license_id == "NOASSERTION":
            license_id = ""
        return {
            "name": metadata.get("name"),
            "url": metadata.get("html_url") or repository_url,
            "hosting": "GitHub",
            "description": metadata.get("description"),
            "created": metadata.get("created_at"),
            "updated": metadata.get("pushed_at"),
            "stars": metadata.get("stargazers_count"),
            "language": metadata.get("language"),
            "license": license_id,
            "archived": metadata.get("archived"),
            "fork": metadata.get("fork"),
            "topics": metadata.get("topics") or [],
            "size": metadata.get("size") or 0,
            "evidence": evidence,
        }
    if host == "gitlab.com":
        project_path = "/".join(parts)
        metadata = client.get(
            f"https://gitlab.com/api/v4/projects/{quote(project_path, safe='')}"
        )
        if metadata.get("archived"):
            return None
        return {
            "name": metadata.get("name"),
            "url": metadata.get("web_url") or repository_url,
            "hosting": "GitLab",
            "description": metadata.get("description"),
            "created": metadata.get("created_at"),
            "updated": metadata.get("last_activity_at"),
            "stars": metadata.get("star_count"),
            "language": "",
            "license": "",
            "archived": metadata.get("archived"),
            "fork": bool(metadata.get("forked_from_project")),
            "topics": metadata.get("topics") or [],
            "size": 0,
            "evidence": evidence,
        }
    if host == "codeberg.org":
        owner, repository = parts[:2]
        metadata = client.get(
            f"https://codeberg.org/api/v1/repos/{quote(owner)}/{quote(repository)}"
        )
        if metadata.get("archived"):
            return None
        return {
            "name": metadata.get("name"),
            "url": metadata.get("html_url") or repository_url,
            "hosting": "Codeberg",
            "description": metadata.get("description"),
            "created": metadata.get("created_at"),
            "updated": metadata.get("updated_at"),
            "stars": metadata.get("stars_count"),
            "language": metadata.get("language"),
            "license": "",
            "archived": metadata.get("archived"),
            "fork": metadata.get("fork"),
            "topics": metadata.get("topics") or [],
            "size": metadata.get("size") or 0,
            "evidence": evidence,
        }
    return None


def telegram_posts(page: str) -> tuple[list[dict[str, Any]], str]:
    chunks = re.split(r'(?=<div class="tgme_widget_message_wrap\b)', page)
    posts: list[dict[str, Any]] = []
    for chunk in chunks:
        post_match = re.search(r'data-post="([^"]+/(\d+))"', chunk)
        date_match = re.search(r'<time datetime="([^"]+)"', chunk)
        if not post_match or not date_match:
            continue
        links = [
            unescape(link)
            for link in re.findall(r'href="(https?://[^"]+)"', chunk)
        ]
        posts.append(
            {
                "id": post_match.group(2),
                "date": iso_date(date_match.group(1)),
                "url": f"https://t.me/{post_match.group(1)}",
                "links": links,
            }
        )
    before_match = re.search(r'data-before="(\d+)"', page)
    return posts, before_match.group(1) if before_match else ""


def telegram_items(
    client: HttpClient,
    source: dict[str, str],
    since: str,
    limit: int,
) -> list[dict[str, Any]]:
    since_date = date.fromisoformat(since)
    base_url = source["Query"].split("?", 1)[0].rstrip("/")
    before = ""
    seen_pages: set[str] = set()
    leads: dict[str, tuple[str, str]] = {}

    while True:
        page_url = f"{base_url}?before={before}" if before else base_url
        if page_url in seen_pages:
            break
        seen_pages.add(page_url)
        posts, next_before = telegram_posts(client.get_text(page_url))
        if not posts:
            break

        dated_posts = [
            post for post in posts
            if post["date"] and date.fromisoformat(post["date"]) >= since_date
        ]
        for post in dated_posts:
            for link in post["links"]:
                repository_url = normalize_repository_url(link)
                if repository_url:
                    leads.setdefault(
                        repository_key(repository_url),
                        (repository_url, post["url"]),
                    )

        oldest = min(date.fromisoformat(post["date"]) for post in posts if post["date"])
        if oldest < since_date or not next_before or len(leads) >= limit:
            break
        before = next_before

    results: list[dict[str, Any]] = []
    for repository_url, evidence in list(leads.values())[:limit]:
        try:
            item = repository_item(client, repository_url, evidence)
        except Exception as error:
            print(
                f"Telegram repository skipped: {repository_url}: {error}",
                file=sys.stderr,
            )
            continue
        if item is None:
            continue
        created = iso_date(item.get("created"))
        updated = iso_date(item.get("updated"))
        if not created or not updated or updated < MIN_LAST_UPDATE:
            print(
                f"Telegram repository skipped: {repository_url}: "
                "missing or stale lifecycle dates",
                file=sys.stderr,
            )
            continue
        results.append(item)
    return results


ADAPTERS = {
    "GitHub": github_items,
    "GitLab": gitlab_items,
    "Codeberg": codeberg_items,
    "MCP Registry": mcp_items,
    "Telegram Channel": telegram_items,
}


def load_sources() -> list[dict[str, str]]:
    with SOURCE_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_candidates(path: Path = CANDIDATE_PATH) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or CANDIDATE_FIELDS), list(reader)


def report_text(new_rows: list[dict[str, str]], errors: list[str], since: str) -> str:
    lines = [
        "# Awesome OSINT Tools Candidate Discovery",
        "",
        f"- Scan date: {date.today().isoformat()}",
        f"- Window start: {since}",
        f"- New candidates: {len(new_rows)}",
        f"- Source errors: {len(errors)}",
        "",
    ]
    if new_rows:
        lines.extend(["| Project | Source | Suggested category | Suggested views | Score | Repository |", "|---|---|---|---|---:|---|"])
        for row in sorted(new_rows, key=lambda item: (-int(item["Score"]), item["Project"].casefold())):
            lines.append(
                f"| {row['Project']} | {row['Discovery Source']} | {row['Suggested Category']} "
                f"| {row['Suggested Views'] or '-'} "
                f"| {row['Score']} | [Review]({row['Repository']}) |"
            )
        lines.append("")
    if errors:
        lines.extend(["## Source errors", ""] + [f"- {error}" for error in errors] + [""])
    lines.append("Candidates remain excluded from the public catalogue until their review status is accepted.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write .catalog/data/candidates.csv")
    parser.add_argument("--lookback-days", type=int, default=14)
    parser.add_argument("--since", help="Override the discovery window start with YYYY-MM-DD")
    parser.add_argument("--max-per-source", type=int, default=100)
    parser.add_argument("--provider", action="append", default=[], help="Limit providers")
    parser.add_argument("--source", action="append", default=[], help="Limit exact configured source names")
    parser.add_argument("--seed-candidates", type=Path, help="Merge candidates from an existing review branch")
    parser.add_argument("--delay", type=float, default=2.1, help="Delay between source requests")
    parser.add_argument("--report", type=Path, help="Write a Markdown discovery report")
    args = parser.parse_args()

    if args.since:
        try:
            since = date.fromisoformat(args.since).isoformat()
        except ValueError:
            print("--since must use YYYY-MM-DD", file=sys.stderr)
            return 2
    else:
        since = (datetime.now(timezone.utc) - timedelta(days=args.lookback_days)).date().isoformat()
    _, catalog_rows = load_catalog()
    fields, existing_candidates = load_candidates()
    if args.seed_candidates and args.seed_candidates.exists():
        seed_fields, seed_candidates = load_candidates(args.seed_candidates)
        if seed_fields != CANDIDATE_FIELDS:
            print(f"Invalid candidate seed schema: {args.seed_candidates}", file=sys.stderr)
            return 2
        existing_keys = {repository_key(row["Repository"]) for row in existing_candidates}
        for row in seed_candidates:
            key = repository_key(row["Repository"])
            if key not in existing_keys:
                existing_candidates.append(row)
                existing_keys.add(key)
    known = {repository_key(row["Repository"]) for row in catalog_rows}
    known.update(repository_key(row["Repository"]) for row in existing_candidates)
    providers = set(args.provider)
    source_names = set(args.source)
    sources = [
        source for source in load_sources()
        if source.get("Enabled", "").casefold() == "true"
        and (not providers or source["Provider"] in providers)
        and (not source_names or source["Name"] in source_names)
    ]

    client = HttpClient(os.environ.get("GITHUB_TOKEN", ""), args.delay)
    new_rows: list[dict[str, str]] = []
    errors: list[str] = []
    for index, source in enumerate(sources, 1):
        adapter = ADAPTERS.get(source["Provider"])
        if adapter is None:
            errors.append(f"{source['Name']}: unsupported provider {source['Provider']}")
            continue
        try:
            items = adapter(client, source, since, args.max_per_source)
        except Exception as error:
            errors.append(f"{source['Name']}: {error}")
            continue
        added = 0
        for item in items:
            if item.get("archived"):
                continue
            url = clean_text(item.get("url"))
            if not url or repository_key(url) in known:
                continue
            dates = lifecycle_dates(item)
            if dates is None:
                print(
                    f"[{source['Name']}] skipped {url}: "
                    "missing or stale lifecycle dates",
                    file=sys.stderr,
                )
                continue
            created, updated = dates
            score = candidate_score(item)
            row = {
                "Project": clean_text(item.get("name")) or url.rstrip("/").rsplit("/", 1)[-1],
                "Repository": url, "Hosting": clean_text(item.get("hosting")),
                "Discovered": date.today().isoformat(), "Discovery Source": source["Name"],
                "Query": source["Query"],
                "Suggested Target Input": source["Suggested Target Input"],
                "Suggested Category": source["Suggested Category"],
                "Suggested Views": source["Suggested Views"],
                "Description": clean_text(item.get("description")), "Created": created,
                "Last Update": updated, "Stars": str(item.get("stars") or 0),
                "Language": clean_text(item.get("language")), "License": clean_text(item.get("license")),
                "Archived": bool_text(item.get("archived")), "Fork": bool_text(item.get("fork")),
                "Score": str(score), "Confidence": confidence(score),
                "Evidence": clean_text(item.get("evidence")) or url,
                "Review Status": "review", "Notes": "",
            }
            new_rows.append(row)
            known.add(repository_key(url))
            added += 1
        print(f"[{index}/{len(sources)}] {source['Name']}: found={len(items)} new={added}")

    all_candidates = existing_candidates + new_rows
    all_candidates.sort(key=lambda row: (row["Review Status"], -int(row["Score"] or 0), row["Project"].casefold()))
    if args.write:
        write_csv(CANDIDATE_PATH, fields or CANDIDATE_FIELDS, all_candidates)
    report = report_text(new_rows, errors, since)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    else:
        print(report)
    print(f"sources={len(sources)} new_candidates={len(new_rows)} errors={len(errors)}")
    return 1 if errors and not new_rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
