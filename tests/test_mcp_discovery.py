from __future__ import annotations

import contextlib
import copy
import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import catalog_common as common
import discover_candidates as discovery


class MCPDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = {
            "Name": "MCP Registry OSINT", "Provider": "MCP Registry", "Enabled": "true",
            "Query": "osint", "Window": "updated", "Suggested Category": "Investigation",
            "Suggested Target Input": "", "Suggested Views": "AGENTIC.md",
        }
        self.payload = {
            "servers": [{
                "server": {"name": "org.example/osint", "version": "1.0.0",
                           "description": "An OSINT MCP server.",
                           "repository": {"url": "https://github.com/example/tool/tree/main", "source": "github"}},
                "_meta": {"io.modelcontextprotocol.registry/official": {
                    "status": "active", "publishedAt": "2026-10-07T12:00:00Z",
                    "updatedAt": "2026-10-08T12:00:00Z", "isLatest": True,
                }},
            }],
            "metadata": {"count": 1},
        }
        self.metadata = {
            "id": 123, "name": "tool", "html_url": "https://github.com/example/tool",
            "description": "Investigates open source evidence.", "created_at": "2026-01-01T12:00:00Z",
            "pushed_at": "2026-10-08T12:00:00Z", "default_branch": "main",
            "stargazers_count": 5, "language": "Python", "license": {"spdx_id": "MIT"},
            "archived": False, "fork": False, "topics": ["osint"], "size": 30,
        }
        self.error: Exception | None = None

    def get(self, client, url: str, github: bool = False):
        if url.startswith("https://registry.modelcontextprotocol.io/"):
            return copy.deepcopy(self.payload)
        if url == "https://api.github.com/repos/example/tool":
            if self.error:
                raise self.error
            return copy.deepcopy(self.metadata)
        if url == "https://api.github.com/repos/example/healthy":
            return {**copy.deepcopy(self.metadata), "html_url": "https://github.com/example/healthy"}
        if url == "https://api.github.com/repos/example/tool/commits/main":
            return {"sha": "abc", "commit": {"committer": {"date": "2026-10-08T12:00:00Z"}}}
        raise AssertionError(f"Unexpected metadata request: {url}")

    def run_discovery(self):
        with tempfile.TemporaryDirectory() as directory:
            candidates = Path(directory) / "candidates.csv"
            common.write_csv(candidates, discovery.CANDIDATE_FIELDS, [])
            original = candidates.read_bytes()
            with (
                patch.object(discovery.HttpClient, "get", lambda client, url, github=False: self.get(client, url, github)),
                patch.object(discovery, "CANDIDATE_PATH", candidates),
                patch.object(discovery, "load_candidates", return_value=(discovery.CANDIDATE_FIELDS, [])),
                patch.object(discovery, "load_catalog", return_value=(common.ALL_COLUMNS, [])),
                patch.object(discovery, "load_sources", return_value=[self.source]),
                patch.object(sys, "argv", ["discover_candidates.py", "--write", "--fail-on-source-error",
                                         "--since", "2026-10-01"]),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                result = discovery.main()
            with candidates.open(newline="") as handle:
                rows = list(csv.DictReader(handle))
            return result, rows, original == candidates.read_bytes()

    def test_registry_entry_reaches_shortlist_using_repository_metadata(self) -> None:
        result, rows, _ = self.run_discovery()
        self.assertEqual(result, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Repository"], "https://github.com/example/tool")
        self.assertEqual(rows[0]["Created"], "2026-01-01")
        self.assertEqual(rows[0]["Last Update"], "2026-10-08")
        self.assertEqual(rows[0]["License"], "MIT")
        self.assertGreaterEqual(int(rows[0]["Score"]), 4)
        self.assertIn("registry.modelcontextprotocol.io", rows[0]["Evidence"])

    def test_multiple_registry_versions_produce_one_normalized_repository(self) -> None:
        version = copy.deepcopy(self.payload["servers"][0])
        version["server"]["version"] = "1.1.0"
        self.payload["servers"].append(version)
        with patch.object(discovery.HttpClient, "get", lambda client, url, github=False: self.get(client, url, github)):
            items = discovery.mcp_items(discovery.HttpClient(), self.source, "2026-10-01", 10)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["url"], "https://github.com/example/tool")

    def test_repository_lookup_error_stops_strict_discovery_without_a_write(self) -> None:
        self.error = RuntimeError("repository metadata unavailable")
        result, rows, unchanged = self.run_discovery()
        self.assertEqual(result, 1)
        self.assertEqual(rows, [])
        self.assertTrue(unchanged)

    def test_unrecognized_registry_dates_are_reported_as_a_source_error(self) -> None:
        self.payload["servers"][0].pop("_meta")
        result, rows, unchanged = self.run_discovery()
        self.assertEqual(result, 1)
        self.assertEqual(rows, [])
        self.assertTrue(unchanged)

    def test_impossible_registry_date_is_reported_without_a_write(self) -> None:
        self.payload["servers"][0]["_meta"]["io.modelcontextprotocol.registry/official"]["updatedAt"] = "2026-13-40T12:00:00Z"
        result, rows, unchanged = self.run_discovery()
        self.assertEqual(result, 1)
        self.assertEqual(rows, [])
        self.assertTrue(unchanged)

    def test_confirmed_missing_repository_does_not_block_healthy_registry_entries(self) -> None:
        healthy = copy.deepcopy(self.payload["servers"][0])
        healthy["server"]["repository"]["url"] = "https://github.com/example/healthy"
        self.payload["servers"].append(healthy)
        self.error = HTTPError("https://api.github.com/repos/example/tool", 404, "Not Found", {}, None)
        self.addCleanup(self.error.close)
        result, rows, _ = self.run_discovery()
        self.assertEqual(result, 0)
        self.assertEqual([row["Repository"] for row in rows], ["https://github.com/example/healthy"])

    def test_server_error_still_blocks_strict_registry_write(self) -> None:
        self.error = HTTPError("https://api.github.com/repos/example/tool", 503, "Unavailable", {}, None)
        self.addCleanup(self.error.close)
        result, rows, unchanged = self.run_discovery()
        self.assertEqual(result, 1)
        self.assertEqual(rows, [])
        self.assertTrue(unchanged)

    def test_archived_repository_is_excluded_after_metadata_lookup(self) -> None:
        self.metadata["archived"] = True
        with patch.object(discovery.HttpClient, "get", lambda client, url, github=False: self.get(client, url, github)):
            items = discovery.mcp_items(discovery.HttpClient(), self.source, "2026-10-01", 10)
        self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
