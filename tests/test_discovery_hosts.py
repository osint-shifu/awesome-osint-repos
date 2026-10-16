from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".catalog/scripts"))
import discover_candidates as discovery


class GitLabDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = {"Query": "osint", "Window": "created"}
        self.item = {
            "id": 123, "name": "tool", "web_url": "https://gitlab.com/example/tool",
            "created_at": "2026-10-10T12:00:00Z", "last_activity_at": "2026-10-15T12:00:00Z",
            "star_count": 5, "topics": ["osint"],
        }
        self.status = {"data": {"project": {"archived": False, "forkedFrom": None}}}

    def discover(self):
        fixture = self
        class Client:
            def get(self, url, github=False):
                if "/api/graphql?" in url:
                    return copy.deepcopy(fixture.status)
                return [copy.deepcopy(fixture.item)]
        return discovery.gitlab_items(Client(), self.source, "2026-10-02", 100)

    def test_created_window_excludes_older_active_repositories(self) -> None:
        self.item["created_at"] = "2020-01-01T12:00:00Z"
        self.assertEqual(self.discover(), [])

    def test_archived_graphql_repository_is_excluded(self) -> None:
        self.status["data"]["project"]["archived"] = True
        self.assertEqual(self.discover(), [])

    def test_fork_status_is_verified_when_rest_omits_it(self) -> None:
        self.status["data"]["project"]["forkedFrom"] = {"id": "gid://gitlab/Project/1"}
        self.assertTrue(self.discover()[0]["fork"])

    def test_missing_status_blocks_discovery(self) -> None:
        self.status = {"data": {"project": {}}}
        with self.assertRaisesRegex(RuntimeError, "status.*verified"):
            self.discover()
