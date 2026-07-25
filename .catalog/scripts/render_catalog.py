#!/usr/bin/env python3
"""Render Markdown catalogue tables and counters from osint-repositories.csv."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from html import escape
from pathlib import Path

from catalog_common import (
    AGENTIC_TABLE_ALIGNMENT,
    AGENTIC_TABLE_HEADER,
    AGENTIC_SECTIONS,
    NEW_PROJECT_LEGEND,
    README_SECTIONS,
    README_TABLE_ALIGNMENT,
    README_TABLE_HEADER,
    ROOT,
    TABLE_ALIGNMENT,
    TABLE_HEADER,
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

CATEGORY_DETAILS = {
    "Identity": ("👤", "Tools centered on people, names, contact identifiers, and identity resolution."),
    "Social Media": ("💬", "Tools for discovering and analyzing public accounts and content on social platforms."),
    "Code Repositories": ("💻", "Tools that investigate public source-code repositories, accounts, and repository metadata."),
    "Infrastructure": ("🌐", "Tools for domains, IP addresses, networks, ASNs, and related internet infrastructure."),
    "Web": ("🔗", "Tools that collect, search, analyze, crawl, or preserve public web content."),
    "Dark Web": ("🧅", "Tools for discovering, collecting, and analyzing onion services and dark-web content."),
    "Threat Intelligence": ("🛡️", "Tools for threat data, indicators, file hashes, vulnerabilities, and malware analysis."),
    "Documents & Records": ("📄", "Tools for documents, files, datasets, public records, extraction, and structured review."),
    "Media": ("🖼️", "Tools for image, video, audio, metadata, verification, and media forensics."),
    "Geolocation": ("📍", "Tools for locations, coordinates, maps, wireless identifiers, aircraft, and satellite data."),
    "Cryptocurrency": ("₿", "Tools for cryptocurrency addresses, blockchain activity, and transaction analysis."),
    "Investigation": ("🔎", "Cross-cutting investigation, case-management, correlation, and research workspaces."),
}


def count_label(count: int) -> str:
    return "project" if count == 1 else "projects"


def replace_update_date(text: str, date: str) -> str:
    if not date:
        return text
    badge_date = date.replace("-", "--")
    text = re.sub(r'alt="Last update: \d{4}-\d{2}-\d{2}"', f'alt="Last update: {date}"', text)
    return re.sub(
        r"(badge/last_update-)\d{4}--\d{2}--\d{2}(-)",
        rf"\g<1>{badge_date}\2",
        text,
    )


def rendered_rows(
    rows: list[dict[str, str]],
    recent_keys: set[str],
    agentic: bool = False,
    readme: bool = False,
) -> list[str]:
    if agentic:
        formatter = format_agentic_markdown_row
    elif readme:
        formatter = format_readme_markdown_row
    else:
        formatter = format_markdown_row
    return [
        formatter(row, repository_key(row["Repository"]) in recent_keys)
        for row in rows
    ]


def anchor_for(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-")


def badge(label: str, slug: str, value: int, color: str, href: str = "") -> str:
    image = (
        f'<img alt="{label}: {value}" '
        f'src="https://img.shields.io/badge/{slug}-{value}-{color}?style=flat-square">'
    )
    return f'<a href="{href}">{image}</a>' if href else image


def navigation(active: str) -> str:
    items = [
        ("Awesome OSINT Tools", "README.md"),
        ("Emerging Projects", "EMERGING.md"),
        ("Agentic AI OSINT", "AGENTIC.md"),
        ("Catalogue Timeline", "TIMELINE.md"),
        ("Repository Database CSV", "osint-repositories.csv"),
    ]
    links = []
    for label, href in items:
        link = f'<a href="{href}">{label}</a>'
        links.append(f"<strong>{link}</strong>" if label == active else link)
    return f"  <p>{' · '.join(links)}</p>"


def append_table(
    lines: list[str],
    selected: list[dict[str, str]],
    recent_keys: set[str],
    agentic: bool = False,
    readme: bool = False,
) -> None:
    if agentic:
        header = AGENTIC_TABLE_HEADER
        alignment = AGENTIC_TABLE_ALIGNMENT
    elif readme:
        header = README_TABLE_HEADER
        alignment = README_TABLE_ALIGNMENT
    else:
        header = TABLE_HEADER
        alignment = TABLE_ALIGNMENT
    lines.extend(
        [
            header,
            alignment,
            *rendered_rows(selected, recent_keys, agentic=agentic, readme=readme),
        ]
    )


def render_readme(
    text: str,
    rows: list[dict[str, str]],
    date: str,
    recent_keys: set[str],
) -> str:
    del text
    counts = {label: len(rows_for_category(rows, category)) for label, category in README_SECTIONS}
    emerging_count = len(rows_for_source(rows, "EMERGING.md"))
    agentic_count = len(rows_for_source(rows, "AGENTIC.md"))
    badge_date = date.replace("-", "--")
    lines = [
        '<a id="top"></a>',
        "",
        '<div align="center">',
        "  <h1>Awesome OSINT Tools</h1>",
        "  <p>A catalogue of open-source OSINT tools organized into 12 clear categories and concrete input types.</p>",
        "  <p>",
        f'    {badge("Emerging projects", "emerging", emerging_count, "bf8700", "EMERGING.md")}',
        f'    {badge("Social Media projects", "social_media", counts["Social Media"], "8250df", "#social-media")}',
        f'    {badge("Agentic integrations", "agentic_integrations", agentic_count, "d1242f", "AGENTIC.md")}',
        f'    {badge("Catalogue projects", "catalogue_projects", len(rows), "8250df")}',
        (
            f'    <img alt="Last update: {date}" src="https://img.shields.io/badge/'
            f'last_update-{badge_date}-1f883d?style=flat-square">'
        ),
        "  </p>",
        navigation("Awesome OSINT Tools"),
        "</div>",
        "",
        "## About this catalogue",
        "",
        (
            "Awesome OSINT Tools is a repository-first catalogue of open-source investigative software. "
            "Every record represents a public source-code repository containing an identifiable tool "
            "or integration with a practical OSINT use case."
        ),
        "",
        (
            "Each project has exactly one value in `Categories`. `Target Input` contains only concrete "
            "data accepted or investigated by the tool, such as `Username`, `Domain`, `IP Address`, "
            "`URL`, `File Hash`, or `Onion Service`. A project may have multiple target inputs."
        ),
        "",
        (
            "`Emerging Projects` and `Agentic AI OSINT` are additional generated views selected through "
            "`Source Files`; they are not category values."
        ),
        "",
        "| File | What it contains |",
        "|---|---|",
        "| [`README.md`](README.md) | Main catalogue with one section for each of the 12 categories. |",
        "| [`EMERGING.md`](EMERGING.md) | Early-stage tools and projects worth monitoring. |",
        "| [`AGENTIC.md`](AGENTIC.md) | Skills, plugins, MCP servers, and AI-agent integrations grouped by main category. |",
        "| [`TIMELINE.md`](TIMELINE.md) | Visual chronology of catalogue additions with descriptions, categories, and current star counts. |",
        "| [`osint-repositories.csv`](osint-repositories.csv) | Canonical repository database in CSV format with all accepted records and current metadata. |",
        "",
        "> [!IMPORTANT]",
        (
            "> Only implementation-bearing repositories with publicly accessible source code are included. "
            "Closed-source services, link collections, courses, articles, prompt-only lists, datasets without "
            "an implemented tool, and repository stubs are excluded."
        ),
        "",
        f"> {NEW_PROJECT_LEGEND}",
        "",
        '<a id="table-of-contents"></a>',
        "",
        "## Table of contents",
        "",
    ]
    for label, _ in README_SECTIONS:
        lines.append(
            f"- [{label}](#{anchor_for(label)}) <sup>{counts[label]} {count_label(counts[label])}</sup>"
        )
    lines.extend(
        [
            f"- [Emerging projects](EMERGING.md) <sup>{emerging_count} {count_label(emerging_count)}</sup>",
            f"- [Agentic AI OSINT](AGENTIC.md) <sup>{agentic_count} {count_label(agentic_count)}</sup>",
            "- [Catalogue timeline](TIMELINE.md)",
            f"- [Complete repository database (CSV)](osint-repositories.csv) <sup>{len(rows)} unique repositories</sup>",
            "",
            "---",
            "",
        ]
    )
    for label, category in README_SECTIONS:
        selected = rows_for_category(rows, category)
        icon, description = CATEGORY_DETAILS[label]
        lines.extend(
            [
                f'<a id="{anchor_for(label)}"></a>',
                "",
                f"## {icon} {label} <sup>{len(selected)} {count_label(len(selected))}</sup>",
                "",
                description,
                "",
            ]
        )
        append_table(lines, selected, recent_keys, readme=True)
        lines.extend(["", '<p align="right"><a href="#table-of-contents">Back to contents ↑</a></p>', ""])
    return "\n".join(lines)


def render_emerging(
    text: str,
    rows: list[dict[str, str]],
    date: str,
    recent_keys: set[str],
) -> str:
    del text
    selected = rows_for_source(rows, "EMERGING.md")
    badge_date = date.replace("-", "--")
    lines = [
        '<a id="top"></a>',
        "",
        '<div align="center">',
        "  <h1>Emerging OSINT Projects</h1>",
        "  <p>A watchlist of early-stage open-source OSINT tools and supporting technologies.</p>",
        "  <p>",
        f'    {badge("Emerging projects", "emerging_projects", len(selected), "bf8700", "#projects")}',
        (
            f'    <img alt="Last update: {date}" src="https://img.shields.io/badge/'
            f'last_update-{badge_date}-1f883d?style=flat-square">'
        ),
        "  </p>",
        navigation("Emerging Projects"),
        "</div>",
        "",
        "## Selection criteria",
        "",
        (
            "Projects listed here have public source code, an identifiable implementation, and a practical "
            "OSINT or investigative use case. Early development, limited adoption, and low star counts do not "
            "automatically exclude a project."
        ),
        "",
        (
            "Membership in this view is stored in `Source Files`. Every project retains one of the 12 main "
            "`Categories` values and its concrete `Target Input` values in the canonical CSV."
        ),
        "",
        f"> {NEW_PROJECT_LEGEND}",
        "",
        '<a id="projects"></a>',
        "",
        f"## Projects <sup>{len(selected)} {count_label(len(selected))}</sup>",
        "",
    ]
    append_table(lines, selected, recent_keys)
    lines.extend(
        [
            "",
            '<p align="right"><a href="#top">Back to top ↑</a></p>',
            "",
            f"[Complete repository database (CSV)](osint-repositories.csv) <sup>{len(rows)} unique repositories</sup>",
            "",
        ]
    )
    return "\n".join(lines)


def render_agentic(
    text: str,
    rows: list[dict[str, str]],
    date: str,
    recent_keys: set[str],
) -> str:
    del text
    selected_all = rows_for_source(rows, "AGENTIC.md")
    active_sections = [
        (label, category, rows_for_source(rows, "AGENTIC.md", category))
        for label, category in AGENTIC_SECTIONS
    ]
    active_sections = [item for item in active_sections if item[2]]
    mcp_count = sum("MCP" in row.get("Type", "") for row in selected_all)
    skill_count = sum("Skill" in row.get("Type", "") for row in selected_all)
    badge_date = date.replace("-", "--")
    lines = [
        '<a id="top"></a>',
        "",
        '<div align="center">',
        "  <h1>Agentic AI OSINT</h1>",
        "  <p>Open-source skills, plugins, MCP servers, and AI-agent integrations for investigative work.</p>",
        "  <p>",
        f'    {badge("Total projects", "total_projects", len(selected_all), "bf8700")}',
        f'    {badge("MCP integrations", "MCP_integrations", mcp_count, "0969da")}',
        f'    {badge("Skill integrations", "skill_integrations", skill_count, "8250df")}',
        (
            f'    <img alt="Last update: {date}" src="https://img.shields.io/badge/'
            f'last_update-{badge_date}-1f883d?style=flat-square">'
        ),
        "  </p>",
        navigation("Agentic AI OSINT"),
        "</div>",
        "",
        "## About this catalogue",
        "",
        (
            "This view contains implementation-bearing repositories that expose investigative workflows or "
            "data access to AI agents. Membership is stored in `Source Files`, while the same single main "
            "category used by the primary catalogue determines the sections below."
        ),
        "",
        (
            "`Target Input` describes the concrete data accepted by a tool. `AI Agent` records the documented "
            "agent runtime or integration surface, such as Claude Code, an Agent Skills-compatible client, or "
            "any MCP-compatible agent."
        ),
        "",
        "> [!IMPORTANT]",
        (
            "> Only public source-code implementations are included. Prompt lists, link collections, closed "
            "services, courses, articles, and repository stubs are excluded."
        ),
        "",
        "> [!NOTE]",
        "> Low or zero star counts do not disqualify a young project with a meaningful implementation.",
        "",
        f"> {NEW_PROJECT_LEGEND}",
        "",
        '<a id="contents"></a>',
        "",
        "## Contents",
        "",
    ]
    for label, _, selected in active_sections:
        lines.append(
            f"- [{label}](#{anchor_for(label)}) <sup>{len(selected)} {count_label(len(selected))}</sup>"
        )
    lines.extend(
        [
            "- [Catalogue timeline](TIMELINE.md)",
            f"- [Complete repository database (CSV)](osint-repositories.csv) <sup>{len(rows)} unique repositories</sup>",
            "",
            "---",
            "",
        ]
    )
    for label, _, selected in active_sections:
        icon, description = CATEGORY_DETAILS[label]
        lines.extend(
            [
                f'<a id="{anchor_for(label)}"></a>',
                "",
                f"## {icon} {label} <sup>{len(selected)} {count_label(len(selected))}</sup>",
                "",
                description,
                "",
            ]
        )
        append_table(lines, selected, recent_keys, agentic=True)
        lines.extend(["", '<p align="right"><a href="#contents">Back to contents ↑</a></p>', ""])
    return "\n".join(lines)


def render_monitoring(
    text: str,
    rows: list[dict[str, str]],
    date: str,
    recent_keys: set[str],
) -> str:
    return replace_update_date(text, date)


def timeline_table_open() -> list[str]:
    return [
        "<table>",
        "  <thead>",
        "    <tr>",
        '      <th align="right">Date</th>',
        '      <th align="center"></th>',
        '      <th align="left">Project</th>',
        "      <th></th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
    ]


def timeline_row(
    row: dict[str, str],
    date_label: str = "",
    date_count: int | None = None,
) -> list[str]:
    project = escape(row["Project"])
    repository = escape(row["Repository"], quote=True)
    description = escape(row["Description"])
    target_inputs = escape(row.get("Target Input", "")) or "-"
    category_labels = " · ".join(
        escape(value) for value in split_values(row["Categories"])
    ) or "-"
    date_cell = ""
    if date_label and date_count is not None:
        date_cell = (
            f"<strong>{escape(date_label)}</strong><br>"
            f"<sub>{date_count} {count_label(date_count)}</sub>"
        )
    return [
        "    <tr>",
        f'      <td align="right" valign="middle">{date_cell}</td>',
        (
            '      <td align="center" valign="middle">│<br>'
            '<img src=".github/assets/new-dot.svg" width="7" height="7" alt="">'
            "<br>│</td>"
        ),
        '      <td valign="middle">',
        f'        <strong><a href="{repository}">{project}</a></strong><br>',
        f"        {description}<br>",
        (
            f"        <sub>Target Input: {target_inputs} · "
            f"Category: {category_labels}</sub>"
        ),
        "      </td>",
        (
            '      <td align="right" valign="top"><strong>⭐&nbsp;'
            f"{stars_as_int(row['Stars']):,}</strong></td>"
        ),
        "    </tr>",
    ]


def timeline_table_close() -> list[str]:
    return [
        "  </tbody>",
        "</table>",
    ]


def render_timeline(
    text: str,
    rows: list[dict[str, str]],
    date: str,
    recent_keys: set[str],
) -> str:
    del text, recent_keys
    dated: dict[str, list[dict[str, str]]] = {}
    legacy: list[dict[str, str]] = []
    for row in rows:
        added = row.get("Added", "")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", added):
            dated.setdefault(added, []).append(row)
        else:
            legacy.append(row)

    dated_count = sum(len(group) for group in dated.values())
    badge_date = date.replace("-", "--")
    lines = [
        '<a id="top"></a>',
        "",
        '<div align="center">',
        "  <h1>Awesome OSINT Tools Timeline</h1>",
        "  <p>A visual chronology of tools added to the catalogue, newest first.</p>",
        "  <p>",
        (
            f'    <img alt="Dated additions: {dated_count}" '
            f'src="https://img.shields.io/badge/dated_additions-'
            f'{dated_count}-0969da?style=flat-square">'
        ),
        (
            f'    <img alt="Catalogue projects: {len(rows)}" '
            f'src="https://img.shields.io/badge/catalogue_projects-'
            f'{len(rows)}-8250df?style=flat-square">'
        ),
        (
            f'    <img alt="Last update: {date}" '
            f'src="https://img.shields.io/badge/last_update-'
            f'{badge_date}-1f883d?style=flat-square">'
        ),
        "  </p>",
        (
            '  <p><strong><a href="TIMELINE.md">Catalogue Timeline</a></strong> · '
            '<a href="README.md">Awesome OSINT Tools</a> · '
            '<a href="EMERGING.md">Emerging Projects</a> · '
            '<a href="AGENTIC.md">Agentic AI OSINT</a> · '
            '<a href="osint-repositories.csv">Repository Database CSV</a></p>'
        ),
        "</div>",
        "",
        (
            "> Each entry shows its catalogue addition date, repository description, "
            "target input, assigned main category, and current star count."
        ),
        (
            "> Projects without a reliable addition date remain available in the "
            "collapsed legacy section."
        ),
        "",
    ]

    lines.extend(timeline_table_open())
    for added in sorted(dated, reverse=True):
        group = sorted(dated[added], key=lambda row: row["Project"].casefold())
        count = len(group)
        for index, row in enumerate(group):
            lines.extend(
                timeline_row(
                    row,
                    date_label=added if index == 0 else "",
                    date_count=count if index == 0 else None,
                )
            )
    lines.extend(timeline_table_close())
    lines.extend(
        [
            "",
            '<p align="right"><a href="#top">Back to top ↑</a></p>',
            "",
        ]
    )

    legacy = sorted(legacy, key=lambda row: row["Project"].casefold())
    legacy_count = len(legacy)
    lines.extend(
        [
            "<details>",
            (
                "<summary><strong>Legacy entries without a catalogue date</strong> "
                f"<sup>{legacy_count} {count_label(legacy_count)}</sup></summary>"
            ),
            "",
            (
                "These projects predate reliable per-entry addition tracking. "
                "They are listed alphabetically without an invented date."
            ),
            "",
        ]
    )
    lines.extend(timeline_table_open())
    for index, row in enumerate(legacy):
        lines.extend(
            timeline_row(
                row,
                date_label="No date" if index == 0 else "",
                date_count=legacy_count if index == 0 else None,
            )
        )
    lines.extend(timeline_table_close())
    lines.extend(
        [
            "",
            "</details>",
            "",
            '<p align="right"><a href="#top">Back to top ↑</a></p>',
            "",
        ]
    )
    return "\n".join(lines)


def rendered_documents() -> dict[Path, str]:
    _, rows = load_catalog()
    date = verified_date(rows)
    recent_keys = recent_repository_keys(rows, date)
    renderers = {
        ROOT / "README.md": render_readme,
        ROOT / "EMERGING.md": render_emerging,
        ROOT / "AGENTIC.md": render_agentic,
        ROOT / "TIMELINE.md": render_timeline,
        ROOT / ".catalog" / "README.md": render_monitoring,
    }
    rendered: dict[Path, str] = {}
    for path, renderer in renderers.items():
        rendered[path] = renderer(
            path.read_text(encoding="utf-8"),
            rows,
            date,
            recent_keys,
        )
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if generated documents differ")
    mode.add_argument("--write", action="store_true", help="Write generated documents")
    args = parser.parse_args()

    changed = 0
    for path, rendered in rendered_documents().items():
        current = path.read_text(encoding="utf-8")
        if current == rendered:
            continue
        changed += 1
        if args.write:
            path.write_text(rendered, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
        else:
            diff = difflib.unified_diff(
                current.splitlines(),
                rendered.splitlines(),
                fromfile=str(path.relative_to(ROOT)),
                tofile=f"generated/{path.relative_to(ROOT)}",
                lineterm="",
            )
            print("\n".join(diff))

    if args.check and changed:
        print(f"{changed} generated document(s) are out of date", file=sys.stderr)
        return 1
    print("catalogue rendering is current" if not changed else f"updated {changed} document(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
