#!/usr/bin/env python3
"""Serve the local Awesome OSINT Repositories catalogue GUI."""

from __future__ import annotations

import argparse
import csv
import json
import threading
import webbrowser
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


GUI_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "osint-repositories.csv"


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def load_catalog() -> dict[str, object]:
    with CATALOG_PATH.open(newline="", encoding="utf-8-sig") as handle:
        records = [dict(row) for row in csv.DictReader(handle)]

    categories = Counter(row.get("Categories", "") for row in records)
    verified_dates = sorted(
        row["Verified"]
        for row in records
        if row.get("Verified", "")
    )
    reference_date = date.fromisoformat(verified_dates[-1]) if verified_dates else date.today()
    recent_cutoff = reference_date - timedelta(days=14)

    recent_count = 0
    for row in records:
        try:
            if date.fromisoformat(row.get("Added", "")) >= recent_cutoff:
                recent_count += 1
        except ValueError:
            continue

    return {
        "records": records,
        "meta": {
            "count": len(records),
            "verified": verified_dates[-1] if verified_dates else "",
            "recent": recent_count,
            "emerging": sum(
                "EMERGING.md" in split_values(row.get("Source Files", ""))
                for row in records
            ),
            "agentic": sum(
                "AGENTIC.md" in split_values(row.get("Source Files", ""))
                for row in records
            ),
            "categories": dict(sorted(categories.items())),
            "source": CATALOG_PATH.name,
            "source_modified": datetime.fromtimestamp(
                CATALOG_PATH.stat().st_mtime,
                tz=timezone.utc,
            ).isoformat(),
        },
    }


class CatalogueHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; base-uri 'none'; "
            "frame-ancestors 'none'; form-action 'none'",
        )
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        super().end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in {"/api/catalog", "/catalog.json"}:
            try:
                body = json.dumps(load_catalog(), ensure_ascii=False).encode("utf-8")
            except (OSError, csv.Error, ValueError) as error:
                body = json.dumps({"error": str(error)}).encode("utf-8")
                self.send_response(500)
            else:
                self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=4173, type=int)
    parser.add_argument("--open", action="store_true", help="Open the GUI in the default browser")
    args = parser.parse_args()

    handler = partial(CatalogueHandler, directory=str(GUI_ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    server.daemon_threads = True
    url = f"http://{args.host}:{args.port}"
    print(f"Awesome OSINT Repositories GUI: {url}")
    print(f"Live data source: {CATALOG_PATH}")
    if args.open:
        threading.Timer(0.3, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
