#!/usr/bin/env python3
"""Create a compact OSINT market-watch report from catalogue state and snapshots."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from catalog_common import DATA_ROOT, load_catalog, repository_key


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def integer(value: str) -> int:
    try:
        return int(value or 0)
    except ValueError:
        return 0


def build_report() -> str:
    _, repositories = load_catalog()
    candidates = load_csv(DATA_ROOT / "candidates.csv")
    snapshots = load_csv(DATA_ROOT / "snapshots.csv")
    today = date.today()
    cutoff = (today - timedelta(days=7)).isoformat()

    snapshot_dates = sorted({row["Date"] for row in snapshots})
    latest_dates = snapshot_dates[-2:]
    by_date: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in snapshots:
        by_date[row["Date"]][repository_key(row["Repository"])] = row

    changes: list[tuple[int, dict[str, str]]] = []
    if len(latest_dates) == 2:
        previous, current = latest_dates
        repository_lookup = {repository_key(row["Repository"]): row for row in repositories}
        for key, current_row in by_date[current].items():
            previous_row = by_date[previous].get(key)
            repository = repository_lookup.get(key)
            if previous_row and repository:
                changes.append((integer(current_row["Stars"]) - integer(previous_row["Stars"]), repository))
        changes.sort(key=lambda item: (-item[0], item[1]["Project"].casefold()))

    recent_candidates = [row for row in candidates if row["Discovered"] >= cutoff]
    review_candidates = [row for row in candidates if row["Review Status"] == "review"]
    archived = [row for row in repositories if row.get("Repository Status") == "archived"]
    unavailable = [row for row in repositories if row.get("Repository Status") == "unavailable"]
    hosting = Counter(row.get("Hosting") or "Unknown" for row in repositories)

    lines = [
        f"# Awesome OSINT Repositories - {today.isoformat()}",
        "",
        f"- Catalogued repositories: {len(repositories)}",
        f"- Candidates awaiting review: {len(review_candidates)}",
        f"- Candidates discovered in the last 7 days: {len(recent_candidates)}",
        f"- Archived repositories: {len(archived)}",
        f"- Unavailable repositories: {len(unavailable)}",
        f"- Hosting coverage: {', '.join(f'{name} {count}' for name, count in sorted(hosting.items()))}",
        "",
    ]

    if changes:
        lines.extend(["## Fastest star growth", "", "| Project | Change | Stars | Repository |", "|---|---:|---:|---|"])
        for delta, row in changes[:10]:
            lines.append(f"| {row['Project']} | {delta:+,} | ⭐ {integer(row['Stars']):,} | [Source]({row['Repository']}) |")
        lines.append("")

    if recent_candidates:
        lines.extend(["## Newly discovered candidates", "", "| Project | Score | Category | Repository |", "|---|---:|---|---|"])
        for row in sorted(recent_candidates, key=lambda item: (-integer(item["Score"]), item["Project"].casefold()))[:25]:
            lines.append(
                f"| {row['Project']} | {row['Score']} | {row['Suggested Category']} | [Review]({row['Repository']}) |"
            )
        lines.append("")

    if unavailable:
        lines.extend(["## Unavailable repositories", ""] + [f"- [{row['Project']}]({row['Repository']})" for row in unavailable] + [""])

    lines.extend(
        [
            "## Review policy",
            "",
            "Discovery is automatic. Publication, removal, descriptions, targets, and compatibility labels remain review-gated.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report()
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
