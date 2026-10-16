from __future__ import annotations

import contextlib
import copy
import io
import os
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from tests import test_metadata_updates as fixtures
import catalog_common as common
import discover_candidates as discovery
import refresh_metadata as refresh


class PublicHostRefreshTests(unittest.TestCase):
    def setUp(self) -> None:
        fixtures.MetadataUpdateTests.setUp(self)
        self.status = {"data": {"project": {"archived": False, "forkedFrom": None}}}
        self.date = "2026-10-10T12:00:00Z"
        self.error = None

    def run_host(self, host: str, *, github_rows=None, token="") -> int:
        hosting = "GitLab" if host == "gitlab.com" else "Codeberg"
        self.row.update(Repository=f"https://{host}/example/tool", Hosting=hosting)
        self.candidate.update(Repository=self.row["Repository"], Hosting=hosting)
        github_rows = github_rows or []
        rows = [*github_rows[:1], self.row, *github_rows[1:]]
        common.write_csv(self.catalogue, common.ALL_COLUMNS, rows)
        common.write_csv(self.candidates, discovery.CANDIDATE_FIELDS, [self.candidate])
        metadata = {
            "id": 123, "web_url": self.row["Repository"], "html_url": self.row["Repository"],
            "created_at": "2026-01-01T12:00:00Z", "default_branch": "main",
            "star_count": 7, "stars_count": 7, "forks_count": 1, "open_issues_count": 2,
        }
        if host == "codeberg.org":
            metadata.update(archived=False, fork=False)
        fixture = self
        def get(client, url, github=False):
            if "/api/graphql?" in url:
                return copy.deepcopy(fixture.status)
            if "/repository/commits?" in url:
                return [{"committed_date": fixture.date}]
            if "/branches/main" in url:
                return {"commit": {"timestamp": fixture.date}}
            if fixture.error:
                raise fixture.error
            return copy.deepcopy(metadata)
        with (
            patch.object(refresh, "ROOT", self.root),
            patch.object(refresh, "CANDIDATE_PATH", self.candidates),
            patch.object(refresh, "SNAPSHOT_PATH", self.snapshots),
            patch.object(refresh, "load_catalog", side_effect=lambda: common.load_catalog(self.catalogue)),
            patch.object(discovery.HttpClient, "get", get),
            patch.dict(os.environ, {"GITHUB_TOKEN": token}),
            patch.object(sys, "argv", ["refresh_metadata.py", "--write", "--snapshot"]),
            contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()),
        ):
            return refresh.main()

    def test_gitlab_refresh_updates_commit_candidates_and_snapshot(self) -> None:
        self.status["data"]["project"]["forkedFrom"] = {"id": "gid://gitlab/Project/1"}
        self.assertEqual(self.run_host("gitlab.com"), 0)
        _, rows = common.load_catalog(self.catalogue)
        self.assertEqual(rows[0]["Last Update"], "2026-10-10")
        self.assertEqual(rows[0]["Fork"], "true")
        self.assertEqual(rows[0]["Stars"], "7")
        self.assertEqual(rows[0]["License"], "MIT")
        self.assertEqual(common.load_catalog(self.candidates)[1][0]["Last Update"], "2026-10-10")
        self.assertEqual(common.load_catalog(self.snapshots)[1][0]["Last Update"], "2026-10-10")

    def test_codeberg_refresh_uses_default_branch_commit(self) -> None:
        self.assertEqual(self.run_host("codeberg.org"), 0)
        row = common.load_catalog(self.catalogue)[1][0]
        self.assertEqual(row["Last Update"], "2026-10-10")
        self.assertEqual(row["Hosting"], "Codeberg")
        self.assertEqual(row["Stars"], "7")

    def test_graphql_results_stay_matched_with_interleaved_public_hosts(self) -> None:
        first, second = fixtures.catalogue_row(), fixtures.catalogue_row()
        first.update(Repository="https://github.com/example/first", **{"Repository ID": "1"})
        second.update(Repository="https://github.com/example/second", **{"Repository ID": "2"})
        def get_graphql(client, repositories):
            values = []
            for owner, name in repositories:
                value = fixtures.github_metadata()
                value.update(id=1 if name == "first" else 2, html_url=f"https://github.com/{owner}/{name}")
                value["_default_branch_committed_at"] = "2026-10-11T12:00:00Z" if name == "first" else "2026-10-12T12:00:00Z"
                values.append(value)
            return values
        with patch.object(refresh.GitHubClient, "get_repositories_graphql", get_graphql):
            self.assertEqual(self.run_host("gitlab.com", github_rows=[first, second], token="test-token"), 0)
        rows = common.load_catalog(self.catalogue)[1]
        self.assertEqual([row["Last Update"] for row in rows], ["2026-10-11", "2026-10-10", "2026-10-12"])

    def test_gitlab_unverified_status_blocks_refresh(self) -> None:
        self.status = {"data": {"project": {}}}
        self.assertEqual(self.run_host("gitlab.com"), 1)
        self.assertEqual(common.load_catalog(self.catalogue)[1][0]["Verified"], "2026-10-05")

    def test_missing_public_branch_commit_blocks_refresh(self) -> None:
        self.date = ""
        self.assertEqual(self.run_host("codeberg.org"), 1)
        self.assertEqual(common.load_catalog(self.catalogue)[1][0]["Verified"], "2026-10-05")

    def test_transient_public_api_failure_does_not_mark_unavailable(self) -> None:
        self.error = HTTPError("https://codeberg.org/api/v1/repos/example/tool", 503, "Unavailable", {}, None)
        self.addCleanup(self.error.close)
        self.assertEqual(self.run_host("codeberg.org"), 1)
        self.assertEqual(common.load_catalog(self.catalogue)[1][0]["Repository Status"], "active")

    def test_confirmed_public_404_marks_unavailable(self) -> None:
        self.error = HTTPError("https://codeberg.org/api/v1/repos/example/tool", 404, "Not Found", {}, None)
        self.addCleanup(self.error.close)
        self.assertEqual(self.run_host("codeberg.org"), 0)
        self.assertEqual(common.load_catalog(self.catalogue)[1][0]["Repository Status"], "unavailable")


class SnapshotIdentityTests(unittest.TestCase):
    def test_same_numeric_id_on_different_hosts_does_not_overwrite_snapshot(self) -> None:
        rows = []
        refresh.update_snapshot(rows, {"Date": "2026-10-16", "Repository ID": "123", "Repository": "https://github.com/example/tool"})
        refresh.update_snapshot(rows, {"Date": "2026-10-16", "Repository ID": "123", "Repository": "https://gitlab.com/example/tool"})
        self.assertEqual(len(rows), 2)

    def test_same_host_rename_updates_existing_snapshot(self) -> None:
        rows = [{"Date": "2026-10-16", "Repository ID": "123", "Repository": "https://github.com/old/tool"}]
        refresh.update_snapshot(rows, {"Date": "2026-10-16", "Repository ID": "123", "Repository": "https://github.com/new/tool"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["Repository"], "https://github.com/new/tool")
