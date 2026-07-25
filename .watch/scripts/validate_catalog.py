#!/usr/bin/env python3
"""Validate catalogue CSV data and generated Markdown tables."""

from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

from catalog_common import (
    AGENTIC_TABLE_ALIGNMENT,
    AGENTIC_TABLE_HEADER,
    AGENTIC_SECTIONS,
    ALL_CATEGORIES,
    ALL_COLUMNS,
    DATA_ROOT,
    MIN_LAST_UPDATE,
    NEW_PROJECT_LEGEND,
    NEW_PROJECT_MARKER,
    WATCH_ROOT,
    README_SECTIONS,
    README_TABLE_ALIGNMENT,
    README_TABLE_HEADER,
    ROOT,
    TABLE_ALIGNMENT,
    TABLE_HEADER,
    canonical_source_files,
    canonical_target_inputs,
    categories,
    format_agentic_markdown_row,
    format_markdown_row,
    format_readme_markdown_row,
    load_catalog,
    recent_repository_keys,
    repository_key,
    rows_for_category,
    rows_for_source,
    split_values,
    stars_as_int,
    verified_date,
)


DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^]]+)\]\(([^)]+)\)")


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def parse_markdown_tables(path: Path, validation: Validation) -> dict[str, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    tables: dict[str, list[str]] = {}
    current_heading = ""
    for index, line in enumerate(lines):
        if line.startswith("## "):
            current_heading = re.sub(r"\s*<sup>.*?</sup>\s*$", "", line[3:]).strip()
            current_heading = re.sub(r"^[^\w]+", "", current_heading)
        table_schemas = {
            TABLE_HEADER: (TABLE_ALIGNMENT, 7),
            README_TABLE_HEADER: (README_TABLE_ALIGNMENT, 7),
            AGENTIC_TABLE_HEADER: (AGENTIC_TABLE_ALIGNMENT, 7),
        }
        if line not in table_schemas:
            continue
        expected_alignment, expected_cells = table_schemas[line]
        validation.check(
            index + 1 < len(lines) and lines[index + 1] == expected_alignment,
            f"{path.name}:{index + 1}: invalid table alignment row",
        )
        rows: list[str] = []
        cursor = index + 2
        marker_pattern = (
            r'(?:<img src="\.github/assets/new-dot\.svg"[^>]*>'
            r"|<sup>🟢</sup>|🟢) "
        )
        while cursor < len(lines) and re.match(
            rf"^\| (?:{marker_pattern})?\[",
            lines[cursor],
        ):
            cells = [cell.strip() for cell in lines[cursor].strip().strip("|").split("|")]
            validation.check(
                len(cells) == expected_cells,
                f"{path.name}:{cursor + 1}: expected {expected_cells} table cells, found {len(cells)}",
            )
            rows.append(lines[cursor])
            cursor += 1
        tables[current_heading] = rows
    return tables


def find_heading_table(tables: dict[str, list[str]], label: str) -> list[str] | None:
    if label in tables:
        return tables[label]
    for heading, rows in tables.items():
        if heading.endswith(f" {label}"):
            return rows
    return None


def validate_catalog(validation: Validation) -> tuple[list[str], list[dict[str, str]]]:
    fields, rows = load_catalog()
    validation.check(fields == ALL_COLUMNS, "osint-repositories.csv: invalid header or column order")

    seen_urls: dict[str, int] = {}
    seen_ids: dict[str, int] = {}
    allowed_status = {"active", "unavailable", "unknown"}
    for line_number, row in enumerate(rows, 2):
        for field in ("Project", "Type", "Description", "Hosting"):
            validation.check(bool(row.get(field, "").strip()), f"osint-repositories.csv:{line_number}: missing {field}")
        key = repository_key(row.get("Repository", ""))
        validation.check(bool(key), f"osint-repositories.csv:{line_number}: missing Repository")
        if key:
            validation.check(key not in seen_urls, f"osint-repositories.csv:{line_number}: duplicate Repository: {row['Repository']}")
            seen_urls[key] = line_number
        parsed = urlparse(row.get("Repository", ""))
        validation.check(parsed.scheme == "https" and bool(parsed.netloc), f"osint-repositories.csv:{line_number}: invalid Repository URL")

        repo_id = row.get("Repository ID", "").strip()
        if repo_id:
            identity = f"{row.get('Hosting', '').casefold()}:{repo_id}"
            validation.check(identity not in seen_ids, f"osint-repositories.csv:{line_number}: duplicate Repository ID: {identity}")
            seen_ids[identity] = line_number

        for field in ("Created", "Last Update", "Verified"):
            value = row.get(field, "")
            validation.check(bool(DATE_PATTERN.fullmatch(value)), f"osint-repositories.csv:{line_number}: invalid {field}: {value!r}")
        added = row.get("Added", "")
        validation.check(
            not added or bool(DATE_PATTERN.fullmatch(added)),
            f"osint-repositories.csv:{line_number}: invalid Added: {added!r}",
        )
        if added and DATE_PATTERN.fullmatch(added):
            validation.check(
                added <= row.get("Verified", ""),
                f"osint-repositories.csv:{line_number}: Added is later than Verified",
            )
        validation.check(
            row.get("Last Update", "") >= MIN_LAST_UPDATE,
            f"osint-repositories.csv:{line_number}: repository is outside the lifecycle window",
        )
        try:
            stars_as_int(row.get("Stars", ""))
        except ValueError:
            validation.errors.append(f"osint-repositories.csv:{line_number}: invalid Stars: {row.get('Stars')!r}")

        row_categories = categories(row)
        validation.check(bool(row_categories), f"osint-repositories.csv:{line_number}: missing Categories")
        validation.check(
            len(row_categories) == 1,
            f"osint-repositories.csv:{line_number}: exactly one main category is required",
        )
        unknown_categories = [value for value in row_categories if value not in ALL_CATEGORIES]
        validation.check(
            not unknown_categories,
            f"osint-repositories.csv:{line_number}: unknown Categories: {', '.join(unknown_categories)}",
        )
        try:
            normalized_targets = canonical_target_inputs(row.get("Target Input", ""))
        except ValueError as error:
            validation.errors.append(f"osint-repositories.csv:{line_number}: {error}")
            normalized_targets = []
        validation.check(
            split_values(row.get("Target Input", "")) == normalized_targets,
            f"osint-repositories.csv:{line_number}: Target Input is not canonical",
        )
        try:
            expected_sources = canonical_source_files(row.get("Source Files", ""))
        except ValueError as error:
            validation.errors.append(f"osint-repositories.csv:{line_number}: {error}")
            expected_sources = []
        actual_sources = split_values(row.get("Source Files", ""))
        validation.check(
            actual_sources == expected_sources and "README.md" in actual_sources,
            f"osint-repositories.csv:{line_number}: Source Files are not canonical",
        )
        if "AGENTIC.md" in actual_sources:
            validation.check(
                bool(row.get("AI Agent", "").strip()),
                f"osint-repositories.csv:{line_number}: AGENTIC.md entry is missing AI Agent",
            )
        validation.check(row.get("Repository Status", "") in allowed_status, f"osint-repositories.csv:{line_number}: invalid Repository Status")
        validation.check(row.get("Review Status", "") == "accepted", f"osint-repositories.csv:{line_number}: canonical records must be accepted")
        validation.check(row.get("Archived", "") == "false", f"osint-repositories.csv:{line_number}: archived repositories must be removed")
        validation.check(row.get("Fork", "") in {"", "true", "false"}, f"osint-repositories.csv:{line_number}: invalid Fork")

    validation.check(len(rows) == len(seen_urls), "osint-repositories.csv: repository uniqueness check failed")
    return fields, rows


def validate_markdown(validation: Validation, rows: list[dict[str, str]]) -> None:
    recent_keys = recent_repository_keys(rows, verified_date(rows))
    specifications = [
        (
            ROOT / "README.md",
            [
                (label, rows_for_category(rows, category), format_readme_markdown_row)
                for label, category in README_SECTIONS
            ],
        ),
        (
            ROOT / "EMERGING.md",
            [("Projects", rows_for_source(rows, "EMERGING.md"), format_markdown_row)],
        ),
        (
            ROOT / "AGENTIC.md",
            [
                (
                    label,
                    rows_for_source(rows, "AGENTIC.md", category),
                    format_agentic_markdown_row,
                )
                for label, category in AGENTIC_SECTIONS
                if rows_for_source(rows, "AGENTIC.md", category)
            ],
        ),
    ]
    for path, sections in specifications:
        tables = parse_markdown_tables(path, validation)
        for label, selected, formatter in sections:
            actual = find_heading_table(tables, label)
            validation.check(actual is not None, f"{path.name}: missing table for {label}")
            if actual is None:
                continue
            expected = [
                formatter(
                    row,
                    repository_key(row["Repository"]) in recent_keys,
                )
                for row in selected
            ]
            validation.check(actual == expected, f"{path.name}: generated rows differ in {label}")

        text = path.read_text(encoding="utf-8")
        validation.check(
            NEW_PROJECT_LEGEND in text,
            f"{path.name}: missing new-project marker legend",
        )

        validation.check(
            not re.search(
                r'^\| (?:<img src="\.github/assets/new-dot\.svg"'
                r'(?=[^>]*align=)[^>]*>|<sup>🟢</sup>|🟢) \[',
                text,
                flags=re.MULTILINE,
            ),
            f"{path.name}: contains legacy dot markers",
        )
def validate_local_links(validation: Validation) -> None:
    for path in (
        ROOT / "README.md",
        ROOT / "EMERGING.md",
        ROOT / "AGENTIC.md",
        ROOT / "TIMELINE.md",
        WATCH_ROOT / "README.md",
    ):
        text = path.read_text(encoding="utf-8")
        for _, target in MARKDOWN_LINK_PATTERN.findall(text):
            if target.startswith(("http://", "https://", "#")):
                continue
            local_path = path.parent / target.split("#", 1)[0]
            validation.check(local_path.exists(), f"{path.name}: missing local link target: {target}")


def validate_timeline(
    validation: Validation,
    rows: list[dict[str, str]],
) -> None:
    path = ROOT / "TIMELINE.md"
    text = path.read_text(encoding="utf-8")
    actual = [
        repository_key(unescape(url))
        for url in re.findall(
            r'<strong><a href="(https://[^"]+)">',
            text,
        )
    ]
    dated_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if DATE_PATTERN.fullmatch(row.get("Added", "")):
            dated_groups[row["Added"]].append(row)
    dated = [
        row
        for added in sorted(dated_groups, reverse=True)
        for row in sorted(
            dated_groups[added],
            key=lambda item: item["Project"].casefold(),
        )
    ]
    legacy = sorted(
        (row for row in rows if not DATE_PATTERN.fullmatch(row.get("Added", ""))),
        key=lambda row: row["Project"].casefold(),
    )
    expected = [repository_key(row["Repository"]) for row in dated + legacy]
    validation.check(
        actual == expected,
        "TIMELINE.md: repository rows are missing, duplicated, or out of chronological order",
    )


def validate_update_badges(
    validation: Validation,
    rows: list[dict[str, str]],
) -> None:
    date = verified_date(rows)
    badge = (
        f'<img alt="Last update: {date}" '
        f'src="https://img.shields.io/badge/last_update-'
        f'{date.replace("-", "--")}-1f883d?style=flat-square">'
    )
    markdown_files = (
        ROOT / "README.md",
        ROOT / "EMERGING.md",
        ROOT / "AGENTIC.md",
        ROOT / "TIMELINE.md",
        WATCH_ROOT / "README.md",
    )
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        validation.check(
            text.count('alt="Last update:') == 1,
            f"{path.relative_to(ROOT)}: expected exactly one Last update badge",
        )
        validation.check(
            badge in text,
            f"{path.relative_to(ROOT)}: missing or outdated Last update badge",
        )


def validate_navigation(validation: Validation) -> None:
    expected = {
        ROOT / "README.md": (
            '<p><strong><a href="README.md">OSINT Tools Watch</a></strong> · '
            '<a href="EMERGING.md">Emerging Projects</a> · '
            '<a href="AGENTIC.md">Agentic AI OSINT</a> · '
            '<a href="TIMELINE.md">Catalogue Timeline</a> · '
            '<a href="osint-repositories.csv">Repository Database CSV</a></p>'
        ),
        ROOT / "EMERGING.md": (
            '<p><a href="README.md">OSINT Tools Watch</a> · '
            '<strong><a href="EMERGING.md">Emerging Projects</a></strong> · '
            '<a href="AGENTIC.md">Agentic AI OSINT</a> · '
            '<a href="TIMELINE.md">Catalogue Timeline</a> · '
            '<a href="osint-repositories.csv">Repository Database CSV</a></p>'
        ),
        ROOT / "AGENTIC.md": (
            '<p><a href="README.md">OSINT Tools Watch</a> · '
            '<a href="EMERGING.md">Emerging Projects</a> · '
            '<strong><a href="AGENTIC.md">Agentic AI OSINT</a></strong> · '
            '<a href="TIMELINE.md">Catalogue Timeline</a> · '
            '<a href="osint-repositories.csv">Repository Database CSV</a></p>'
        ),
        ROOT / "TIMELINE.md": (
            '<p><strong><a href="TIMELINE.md">Catalogue Timeline</a></strong> · '
            '<a href="README.md">OSINT Tools Watch</a> · '
            '<a href="EMERGING.md">Emerging Projects</a> · '
            '<a href="AGENTIC.md">Agentic AI OSINT</a> · '
            '<a href="osint-repositories.csv">Repository Database CSV</a></p>'
        ),
        WATCH_ROOT / "README.md": (
            '<p><strong><a href="README.md">Monitoring</a></strong> · '
            '<a href="../README.md">OSINT Tools Watch</a> · '
            '<a href="../EMERGING.md">Emerging Projects</a> · '
            '<a href="../AGENTIC.md">Agentic AI OSINT</a> · '
            '<a href="../TIMELINE.md">Catalogue Timeline</a> · '
            '<a href="../osint-repositories.csv">Repository Database CSV</a></p>'
        ),
    }
    for path, navigation in expected.items():
        validation.check(
            navigation in path.read_text(encoding="utf-8"),
            f"{path.relative_to(ROOT)}: invalid navigation order or labels",
        )


def validate_auxiliary_csv(
    validation: Validation,
    catalogue: list[dict[str, str]],
) -> None:
    canonical = {repository_key(row["Repository"]): row for row in catalogue}
    canonical_ids = {
        row.get("Repository ID", "") for row in catalogue if row.get("Repository ID", "")
    }
    schemas = {
        DATA_ROOT / "candidates.csv": [
            "Project", "Repository", "Hosting", "Discovered", "Discovery Source", "Query",
            "Suggested Target Input", "Suggested Category", "Suggested Views", "Description", "Created", "Last Update",
            "Stars", "Language", "License", "Archived", "Fork", "Score", "Confidence",
            "Evidence", "Review Status", "Notes",
        ],
        DATA_ROOT / "snapshots.csv": [
            "Date", "Repository ID", "Repository", "Stars", "Forks", "Open Issues",
            "Last Update", "Archived",
        ],
        DATA_ROOT / "sources.csv": [
            "Name", "Provider", "Query", "Window", "Suggested Target Input", "Suggested Category", "Suggested Views", "Enabled",
        ],
    }
    for path, expected in schemas.items():
        validation.check(path.exists(), f"missing automation data file: {path.name}")
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
            rows = list(reader)
        validation.check(header == expected, f"{path.name}: invalid header")
        if path.name == "candidates.csv":
            seen: set[str] = set()
            for line_number, row in enumerate(rows, 2):
                key = repository_key(row.get("Repository", ""))
                validation.check(bool(key) and key not in seen, f"candidates.csv:{line_number}: invalid or duplicate Repository")
                seen.add(key)
                validation.check(bool(DATE_PATTERN.fullmatch(row.get("Discovered", ""))), f"candidates.csv:{line_number}: invalid Discovered")
                validation.check(bool(DATE_PATTERN.fullmatch(row.get("Created", ""))), f"candidates.csv:{line_number}: invalid Created")
                validation.check(bool(DATE_PATTERN.fullmatch(row.get("Last Update", ""))), f"candidates.csv:{line_number}: invalid Last Update")
                validation.check(
                    row.get("Last Update", "") >= MIN_LAST_UPDATE,
                    f"candidates.csv:{line_number}: repository is outside the lifecycle window",
                )
                validation.check(row.get("Review Status") in {"review", "accepted", "rejected"}, f"candidates.csv:{line_number}: invalid Review Status")
                validation.check(row.get("Archived") == "false", f"candidates.csv:{line_number}: archived candidates must be removed")
                validation.check(row.get("Fork") in {"true", "false"}, f"candidates.csv:{line_number}: invalid Fork")
                try:
                    suggested_targets = canonical_target_inputs(row.get("Suggested Target Input", ""))
                except ValueError as error:
                    validation.errors.append(f"candidates.csv:{line_number}: {error}")
                    suggested_targets = []
                validation.check(
                    split_values(row.get("Suggested Target Input", "")) == suggested_targets,
                    f"candidates.csv:{line_number}: Suggested Target Input is not canonical",
                )
                validation.check(
                    row.get("Suggested Category", "") in ALL_CATEGORIES,
                    f"candidates.csv:{line_number}: unknown Suggested Category",
                )
                suggested_views = split_values(row.get("Suggested Views", ""))
                try:
                    normalized_views = canonical_source_files(suggested_views)
                except ValueError as error:
                    validation.errors.append(f"candidates.csv:{line_number}: {error}")
                    normalized_views = []
                validation.check(
                    suggested_views == normalized_views
                    and "README.md" not in suggested_views,
                    f"candidates.csv:{line_number}: unknown Suggested Views",
                )
                if row.get("Review Status") == "accepted":
                    current = canonical.get(key)
                    validation.check(current is not None, f"candidates.csv:{line_number}: accepted candidate is missing from canonical data")
                    if current is not None:
                        for field in (
                            "Hosting",
                            "Created",
                            "Last Update",
                            "Stars",
                            "License",
                            "Archived",
                            "Fork",
                        ):
                            validation.check(
                                row.get(field, "") == current.get(field, ""),
                                f"candidates.csv:{line_number}: {field} differs from canonical data",
                            )
                try:
                    stars_as_int(row.get("Stars", ""))
                    int(row.get("Score", ""))
                except ValueError:
                    validation.errors.append(f"candidates.csv:{line_number}: invalid numeric value")
        elif path.name == "snapshots.csv":
            seen_snapshots: set[tuple[str, str]] = set()
            for line_number, row in enumerate(rows, 2):
                identity = row.get("Repository ID") or repository_key(row.get("Repository", ""))
                snapshot_key = (row.get("Date", ""), identity)
                validation.check(
                    bool(identity) and snapshot_key not in seen_snapshots,
                    f"snapshots.csv:{line_number}: invalid or duplicate snapshot",
                )
                seen_snapshots.add(snapshot_key)
                validation.check(bool(DATE_PATTERN.fullmatch(row.get("Date", ""))), f"snapshots.csv:{line_number}: invalid Date")
                validation.check(bool(DATE_PATTERN.fullmatch(row.get("Last Update", ""))), f"snapshots.csv:{line_number}: invalid Last Update")
                validation.check(
                    repository_key(row.get("Repository", "")) in canonical
                    or row.get("Repository ID", "") in canonical_ids,
                    f"snapshots.csv:{line_number}: snapshot repository is missing from canonical data",
                )
                validation.check(row.get("Archived") == "false", f"snapshots.csv:{line_number}: archived snapshots must be removed")
                try:
                    stars_as_int(row.get("Stars", ""))
                except ValueError:
                    validation.errors.append(f"snapshots.csv:{line_number}: invalid Stars")
        elif path.name == "sources.csv":
            seen_names: set[str] = set()
            for line_number, row in enumerate(rows, 2):
                name = row.get("Name", "")
                validation.check(bool(name) and name not in seen_names, f"sources.csv:{line_number}: missing or duplicate Name")
                seen_names.add(name)
                validation.check(
                    row.get("Provider")
                    in {"GitHub", "GitLab", "Codeberg", "MCP Registry", "Telegram Channel"},
                    f"sources.csv:{line_number}: unsupported Provider",
                )
                validation.check(bool(row.get("Query", "")), f"sources.csv:{line_number}: missing Query")
                validation.check(row.get("Window") in {"created", "pushed", "updated"}, f"sources.csv:{line_number}: invalid Window")
                try:
                    suggested_targets = canonical_target_inputs(row.get("Suggested Target Input", ""))
                except ValueError as error:
                    validation.errors.append(f"sources.csv:{line_number}: {error}")
                    suggested_targets = []
                validation.check(
                    split_values(row.get("Suggested Target Input", "")) == suggested_targets,
                    f"sources.csv:{line_number}: Suggested Target Input is not canonical",
                )
                validation.check(
                    row.get("Suggested Category", "") in ALL_CATEGORIES,
                    f"sources.csv:{line_number}: unknown Suggested Category",
                )
                suggested_views = split_values(row.get("Suggested Views", ""))
                try:
                    normalized_views = canonical_source_files(suggested_views)
                except ValueError as error:
                    validation.errors.append(f"sources.csv:{line_number}: {error}")
                    normalized_views = []
                validation.check(
                    suggested_views == normalized_views
                    and "README.md" not in suggested_views,
                    f"sources.csv:{line_number}: unknown Suggested Views",
                )
                validation.check(row.get("Enabled", "").casefold() in {"true", "false"}, f"sources.csv:{line_number}: invalid Enabled")


def main() -> int:
    validation = Validation()
    _, rows = validate_catalog(validation)
    validate_markdown(validation, rows)
    validate_local_links(validation)
    validate_timeline(validation, rows)
    validate_update_badges(validation, rows)
    validate_navigation(validation)
    validate_auxiliary_csv(validation, rows)
    validation.check(
        (ROOT / ".github" / "assets" / "new-dot.svg").exists(),
        "missing new-project marker asset",
    )
    validation.check(not (ROOT / "SOCIAL.md").exists(), "SOCIAL.md must remain merged into README.md")

    if validation.errors:
        print("Catalogue validation failed:", file=sys.stderr)
        for error in validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Catalogue validation passed: {len(rows)} unique repositories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
