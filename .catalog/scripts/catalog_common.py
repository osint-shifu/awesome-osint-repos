#!/usr/bin/env python3
"""Shared catalogue parsing and formatting helpers."""

from __future__ import annotations

import csv
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
CATALOG_ROOT = ROOT / ".catalog"
DATA_ROOT = CATALOG_ROOT / "data"
CATALOG_PATH = ROOT / "osint-repositories.csv"
MIN_LAST_UPDATE = "2020-01-01"
NEW_PROJECT_WINDOW_DAYS = 14
NEW_PROJECT_MARKER = (
    '<img src=".github/assets/new-dot.svg" width="6" height="6" alt="">'
)
NEW_PROJECT_LEGEND = (
    f"{NEW_PROJECT_MARKER} marks projects added to the catalogue within the last 14 days."
)

PUBLIC_COLUMNS = [
    "Project",
    "Repository",
    "Description",
    "Target Input",
    "Categories",
    "Type",
    "AI Agent",
    "License",
    "Stars",
    "Created",
    "Last Update",
    "Added",
]

MONITOR_COLUMNS = [
    "Verified",
    "Hosting",
    "Repository ID",
    "Archived",
    "Fork",
    "Repository Status",
    "Review Status",
    "Discovery Source",
    "Source Files",
]

PLATFORM_COLUMNS = [
    "Platform",
]

ALL_COLUMNS = PUBLIC_COLUMNS + MONITOR_COLUMNS + PLATFORM_COLUMNS

TABLE_HEADER = (
    "| Project | Target Input | Categories | Description | Created | Last Update | Stars |"
)
TABLE_ALIGNMENT = "|:---|:---|:---:|:---|:---:|:---:|---:|"
README_TABLE_HEADER = (
    "| Project | Type | Target Input | Description | Created | Last Update | Stars |"
)
README_TABLE_ALIGNMENT = "|:---|:---|:---|:---|:---:|:---:|---:|"
AGENTIC_TABLE_HEADER = (
    "| Project | Target Input | AI Agent | Description | Created | Last Update | Stars |"
)
AGENTIC_TABLE_ALIGNMENT = "|:---|:---|:---|:---|:---:|:---:|---:|"

README_SECTIONS = [
    ("Identity", "Identity"),
    ("Social Media", "Social Media"),
    ("Code Repositories", "Code Repositories"),
    ("Infrastructure", "Infrastructure"),
    ("Web", "Web"),
    ("Dark Web", "Dark Web"),
    ("Threat Intelligence", "Threat Intelligence"),
    ("Documents & Records", "Documents & Records"),
    ("Media", "Media"),
    ("Geolocation", "Geolocation"),
    ("Cryptocurrency", "Cryptocurrency"),
    ("Investigation", "Investigation"),
]

AGENTIC_SECTIONS = README_SECTIONS

BASE_CATEGORIES = [category for _, category in README_SECTIONS]
ALL_CATEGORIES = set(BASE_CATEGORIES)
TARGET_INPUTS = {
    "Name",
    "Username",
    "Email",
    "Phone Number",
    "Domain",
    "IP Address",
    "ASN",
    "CIDR",
    "URL",
    "Onion Service",
    "Image",
    "Location",
    "BSSID / SSID",
    "Organization Name",
    "Crypto Address",
    "File Hash",
    "Document",
    "Keyword",
    "Video",
    "Repository URL",
    "Event Data",
    "Coordinates",
    "Dataset",
    "CVE ID",
    "File",
    "Audio",
    "Text",
    "Aircraft ID",
}
SOURCE_FILE_ORDER = ["README.md", "EMERGING.md", "AGENTIC.md"]

# Platform is a rendering dimension inside the Social Media category, not a
# thirteenth category. A blank value means the tool is deliberately
# cross-platform, never that it is unclassified.
PLATFORM_CATEGORY = "Social Media"
CROSS_PLATFORM_LABEL = "Cross-platform"
PLATFORMS = {
    "Telegram",
    "Instagram",
    "X / Twitter",
    "LinkedIn",
    "YouTube",
    "Discord",
    "Reddit",
    "Steam",
    "TikTok",
    "Snapchat",
    "WhatsApp",
}


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def canonical_target_inputs(value: str | Iterable[str]) -> list[str]:
    raw_values = split_values(value) if isinstance(value, str) else list(value)
    normalized: list[str] = []
    for raw_value in raw_values:
        target = raw_value.strip()
        if target not in TARGET_INPUTS:
            raise ValueError(f"Unknown Target Input: {target}")
        if target not in normalized:
            normalized.append(target)
    return normalized


def canonical_source_files(value: str | Iterable[str]) -> list[str]:
    raw_values = split_values(value) if isinstance(value, str) else list(value)
    unknown = [item for item in raw_values if item not in SOURCE_FILE_ORDER]
    if unknown:
        raise ValueError(f"Unknown Source Files: {', '.join(unknown)}")
    return [item for item in SOURCE_FILE_ORDER if item in raw_values]


def canonical_platform(value: str) -> str:
    platform = (value or "").strip()
    if platform and platform not in PLATFORMS:
        raise ValueError(f"Unknown Platform: {platform}")
    return platform


def misplaced_platform(row: dict[str, str]) -> bool:
    """A platform only carries meaning inside the Social Media category."""
    return bool((row.get("Platform") or "").strip()) and row.get("Categories", "") != PLATFORM_CATEGORY


def platform_groups(rows: Iterable[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    """Group Social Media rows into a cross-platform bucket and per-platform buckets.

    The cross-platform bucket leads because the catalogue's most used social
    tools search hundreds of sites and belong to no single platform. Remaining
    groups follow by descending size so the busiest platforms surface first,
    with alphabetical order breaking ties for a stable render.
    """
    buckets: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        buckets.setdefault(row.get("Platform", "").strip(), []).append(row)

    ordered: list[tuple[str, list[dict[str, str]]]] = []
    if buckets.get(""):
        ordered.append((CROSS_PLATFORM_LABEL, buckets.pop("")))
    buckets.pop("", None)
    for platform in sorted(buckets, key=lambda name: (-len(buckets[name]), name.casefold())):
        ordered.append((platform, buckets[platform]))
    return [
        (label, sorted(group, key=lambda row: -stars_as_int(row.get("Stars", "0"))))
        for label, group in ordered
    ]


def load_catalog(path: Path = CATALOG_PATH) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Missing CSV header: {path}")
        rows = [{key: value or "" for key, value in row.items()} for row in reader]
        return list(reader.fieldnames), rows


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def categories(row: dict[str, str]) -> list[str]:
    return split_values(row.get("Categories", ""))


def source_files(row: dict[str, str]) -> list[str]:
    return split_values(row.get("Source Files", ""))


def rows_for_category(rows: Iterable[dict[str, str]], category: str) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if category in categories(row) and row.get("Review Status", "accepted") == "accepted"
    ]
    # CSV order is the deterministic tiebreaker so equal-star projects do not
    # jump around when the renderer runs.
    return sorted(selected, key=lambda row: -stars_as_int(row.get("Stars", "0")))


def rows_for_source(
    rows: Iterable[dict[str, str]],
    source_file: str,
    category: str = "",
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if source_file in source_files(row)
        and (not category or row.get("Categories", "") == category)
        and row.get("Review Status", "accepted") == "accepted"
    ]
    return sorted(selected, key=lambda row: -stars_as_int(row.get("Stars", "0")))


def stars_as_int(value: str) -> int:
    cleaned = value.replace(",", "").strip()
    return int(cleaned or "0")


def markdown_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def format_markdown_row(row: dict[str, str], is_new: bool = False) -> str:
    marker = f"{NEW_PROJECT_MARKER} " if is_new else ""
    project = f"{marker}[{markdown_text(row['Project'])}]({row['Repository']})"
    return (
        f"| {project} "
        f"| {markdown_text(row['Target Input']) or '-'} "
        f"| {markdown_text(row['Categories'])} "
        f"| {markdown_text(row['Description'])} "
        f"| {row['Created']} | {row['Last Update']} "
        f"| ⭐ {stars_as_int(row['Stars']):,} |"
    )


def format_readme_markdown_row(row: dict[str, str], is_new: bool = False) -> str:
    marker = f"{NEW_PROJECT_MARKER} " if is_new else ""
    project = f"{marker}[{markdown_text(row['Project'])}]({row['Repository']})"
    return (
        f"| {project} "
        f"| {markdown_text(row['Type']) or '-'} "
        f"| {markdown_text(row['Target Input']) or '-'} "
        f"| {markdown_text(row['Description'])} "
        f"| {row['Created']} | {row['Last Update']} "
        f"| ⭐ {stars_as_int(row['Stars']):,} |"
    )


def format_agentic_markdown_row(row: dict[str, str], is_new: bool = False) -> str:
    marker = f"{NEW_PROJECT_MARKER} " if is_new else ""
    project = f"{marker}[{markdown_text(row['Project'])}]({row['Repository']})"
    return (
        f"| {project} "
        f"| {markdown_text(row['Target Input']) or '-'} "
        f"| {markdown_text(row['AI Agent']) or '-'} "
        f"| {markdown_text(row['Description'])} "
        f"| {row['Created']} | {row['Last Update']} "
        f"| ⭐ {stars_as_int(row['Stars']):,} |"
    )


def verified_date(rows: Iterable[dict[str, str]]) -> str:
    values = [row.get("Verified", "") for row in rows]
    valid = sorted(value for value in values if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    if valid:
        return valid[-1]
    return ""


def repository_key(url: str) -> str:
    return url.strip().lower().removesuffix("/").removesuffix(".git")


def recent_repository_keys(
    rows: Iterable[dict[str, str]],
    reference_date: str,
    window_days: int = NEW_PROJECT_WINDOW_DAYS,
) -> set[str]:
    if not reference_date:
        return set()

    current = date.fromisoformat(reference_date)
    earliest = current - timedelta(days=window_days - 1)
    return {
        repository_key(row.get("Repository", ""))
        for row in rows
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", row.get("Added", ""))
        and earliest <= date.fromisoformat(row["Added"]) <= current
    }
