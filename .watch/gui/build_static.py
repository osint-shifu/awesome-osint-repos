#!/usr/bin/env python3
"""Build a dependency-free static OSINT Tools Watch site."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from server import GUI_ROOT, load_catalog


DIST_ROOT = GUI_ROOT / "dist"
STATIC_FILES = ("index.html", "styles.css", "app.js", "favicon.svg")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--domain",
        help="Write a CNAME file for hosts that support it, for example osint-tools.example.com",
    )
    args = parser.parse_args()

    DIST_ROOT.mkdir(exist_ok=True)
    for name in STATIC_FILES:
        shutil.copy2(GUI_ROOT / name, DIST_ROOT / name)

    (DIST_ROOT / "catalog.json").write_text(
        json.dumps(load_catalog(), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    cname = DIST_ROOT / "CNAME"
    if args.domain:
        cname.write_text(f"{args.domain.strip()}\n", encoding="utf-8")
    elif cname.exists():
        cname.unlink()

    print(f"Static site built: {DIST_ROOT}")
    print(f"Records: {load_catalog()['meta']['count']}")
    if args.domain:
        print(f"Custom domain: {args.domain.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
