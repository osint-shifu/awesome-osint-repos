from __future__ import annotations

import contextlib
import copy
import csv
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import catalog_common as common
import discover_candidates as discovery
import refresh_metadata as refresh
import review_candidate as review


def catalogue_row() -> dict[str, str]:
    row = dict.fromkeys(common.ALL_COLUMNS, "")
    row.update(
        Project="Tool", Repository="https://github.com/old/tool",
        Description="Examines investigative evidence.", Categories="Investigation",
        Type="Python CLI", Hosting="GitHub", License="MIT", Stars="5",
        Created="2026-01-01", Added="2026-10-01", Verified="2026-10-05",
        **{"Last Update": "2026-10-04", "Repository ID": "123", "Archived": "false",
           "Fork": "false", "Repository Status": "active", "Review Status": "accepted",
           "Source Files": "README.md", "Discovery Source": "Manual review"},
    )
    return row


def github_metadata() -> dict[str, object]:
    return {
        "id": 123, "name": "tool", "html_url": "https://github.com/old/tool",
        "created_at": "2026-01-01T12:00:00Z", "pushed_at": "2026-10-08T12:00:00Z",
        "default_branch": "main", "stargazers_count": 6, "license": {"spdx_id": "MIT"},
        "archived": False, "fork": False, "forks_count": 1, "open_issues_count": 2,
        "_default_branch_checked": True, "_default_branch_committed_at": "2026-10-08T12:00:00Z",
    }


class MetadataUpdateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.catalogue = self.root / "osint-repositories.csv"
        self.candidates = self.root / "candidates.csv"
        self.snapshots = self.root / "snapshots.csv"
        self.row = catalogue_row()
        self.candidate = dict.fromkeys(discovery.CANDIDATE_FIELDS, "")
        self.candidate.update({key: value for key, value in self.row.items() if key in self.candidate})
        self.candidate.update(Language="Python", Score="8", Confidence="high", Notes="Reviewed implementation.")
        common.write_csv(self.catalogue, common.ALL_COLUMNS, [self.row])
        common.write_csv(self.candidates, discovery.CANDIDATE_FIELDS, [self.candidate])
        common.write_csv(self.snapshots, refresh.SNAPSHOT_FIELDS, [])

    def run_refresh(self, metadata: dict[str, object], *, snapshot: bool = False, extra: list[str] | None = None) -> int:
        arguments = ["refresh_metadata.py", "--write"]
        arguments.extend(extra or [])
        if snapshot:
            arguments.append("--snapshot")
        with (
            patch.object(refresh, "ROOT", self.root),
            patch.object(refresh, "CANDIDATE_PATH", self.candidates),
            patch.object(refresh, "SNAPSHOT_PATH", self.snapshots),
            patch.object(refresh, "load_catalog", side_effect=lambda: common.load_catalog(self.catalogue)),
            patch.object(refresh.GitHubClient, "get_repository", return_value=(200, metadata)),
            patch.object(refresh.GitHubClient, "get_default_branch_commit", return_value=(409, None)),
            patch.dict(os.environ, {"GITHUB_TOKEN": ""}),
            patch.object(sys, "argv", arguments),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return refresh.main()

    def test_missing_graphql_commit_date_does_not_write_or_advance_verified(self) -> None:
        metadata = github_metadata()
        metadata["_default_branch_committed_at"] = ""
        original = self.catalogue.read_bytes()
        self.assertEqual(self.run_refresh(metadata), 1)
        self.assertEqual(self.catalogue.read_bytes(), original)

    def test_missing_rest_branch_commit_does_not_write(self) -> None:
        metadata = github_metadata()
        metadata.pop("_default_branch_checked")
        metadata.pop("_default_branch_committed_at")
        original = self.catalogue.read_bytes()
        self.assertEqual(self.run_refresh(metadata), 1)
        self.assertEqual(self.catalogue.read_bytes(), original)

    def test_missing_repository_payload_is_not_a_confirmed_404(self) -> None:
        original = self.catalogue.read_bytes()
        self.assertEqual(self.run_refresh(None), 1)
        self.assertEqual(self.catalogue.read_bytes(), original)

    def test_confirmed_archived_repository_can_be_removed_without_a_commit_date(self) -> None:
        metadata = github_metadata()
        metadata.update(archived=True, _default_branch_committed_at="")
        self.assertEqual(self.run_refresh(metadata, extra=["--drop-archived"]), 0)
        self.assertEqual(common.load_catalog(self.catalogue)[1], [])
        self.assertEqual(common.load_catalog(self.candidates)[1], [])

    def test_renamed_stale_repository_is_removed_with_its_candidate(self) -> None:
        metadata = github_metadata()
        metadata.update(html_url="https://github.com/new/tool", _default_branch_committed_at="2019-01-01T12:00:00Z")
        self.assertEqual(self.run_refresh(metadata, extra=["--drop-stale-before", "2020-01-01"]), 0)
        self.assertEqual(common.load_catalog(self.catalogue)[1], [])
        self.assertEqual(common.load_catalog(self.candidates)[1], [])

    def test_rename_preserves_accepted_candidate_and_review_notes(self) -> None:
        metadata = github_metadata()
        metadata["html_url"] = "https://github.com/new/tool"
        self.assertEqual(self.run_refresh(metadata, snapshot=True), 0)
        with self.candidates.open(newline="") as handle:
            candidates = list(csv.DictReader(handle))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["Repository"], "https://github.com/new/tool")
        self.assertEqual(candidates[0]["Review Status"], "accepted")
        self.assertEqual(candidates[0]["Notes"], "Reviewed implementation.")

    def test_rename_merges_duplicate_lead_without_losing_the_accepted_decision(self) -> None:
        lead = {**self.candidate, "Repository": "https://github.com/new/tool",
                "Review Status": "review", "Notes": "Found in registry."}
        common.write_csv(self.candidates, discovery.CANDIDATE_FIELDS, [self.candidate, lead])
        metadata = github_metadata()
        metadata["html_url"] = "https://github.com/new/tool"
        self.assertEqual(self.run_refresh(metadata), 0)
        with self.candidates.open(newline="") as handle:
            candidates = list(csv.DictReader(handle))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["Review Status"], "accepted")
        self.assertIn("Reviewed implementation.", candidates[0]["Notes"])
        self.assertIn("Found in registry.", candidates[0]["Notes"])

    def fail_replace(self, destination: Path):
        real_replace = Path.replace

        def replace(path: Path, target: Path) -> Path:
            if Path(target) == destination:
                raise OSError("injected replacement failure")
            return real_replace(path, target)

        return patch.object(Path, "replace", replace)

    def test_refresh_rolls_back_catalogue_and_candidates_when_snapshot_publish_fails(self) -> None:
        paths = (self.catalogue, self.candidates, self.snapshots)
        original = [path.read_bytes() for path in paths]
        with self.fail_replace(self.snapshots):
            try:
                result = self.run_refresh(github_metadata(), snapshot=True)
            except OSError:
                result = 1
        self.assertEqual(result, 1)
        self.assertEqual([path.read_bytes() for path in paths], original)

    def test_acceptance_rolls_back_catalogue_when_candidate_publish_fails(self) -> None:
        common.write_csv(self.catalogue, common.ALL_COLUMNS, [])
        self.candidate["Review Status"] = "review"
        common.write_csv(self.candidates, discovery.CANDIDATE_FIELDS, [self.candidate])
        original = self.catalogue.read_bytes(), self.candidates.read_bytes()
        with (
            patch.object(review, "ROOT", self.root),
            patch.object(review, "CANDIDATE_PATH", self.candidates),
            patch.object(review, "load_catalog", side_effect=lambda: common.load_catalog(self.catalogue)),
            patch.object(review, "refresh_candidate_metadata", return_value="123"),
            patch.object(sys, "argv", ["review_candidate.py", "https://github.com/old/tool", "--accept",
                                     "--category", "Investigation", "--type", "Python CLI",
                                     "--description", "Examines investigative evidence."]),
            self.fail_replace(self.candidates),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            try:
                result = review.main()
            except OSError:
                result = 1
        self.assertEqual(result, 1)
        self.assertEqual((self.catalogue.read_bytes(), self.candidates.read_bytes()), original)


class GitLabVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.metadata = {
            "id": 123, "name": "Tool", "web_url": "https://gitlab.com/example/tool",
            "created_at": "2026-01-01T12:00:00Z", "default_branch": "main",
            "star_count": 2, "visibility": "public", "topics": ["osint"],
        }
        self.candidate = {"Repository": "https://gitlab.com/example/tool", "Archived": "", "Fork": ""}

    def verify(self, status: dict[str, object]) -> str:
        def get(client, url: str, github: bool = False):
            if "/api/graphql" in url:
                return status
            if "/repository/commits?" in url:
                return [{"id": "abc", "committed_date": "2026-10-08T12:00:00Z"}]
            return copy.deepcopy(self.metadata)

        with patch.object(review.HttpClient, "get", get):
            return review.refresh_gitlab_candidate(self.candidate)

    def test_missing_archival_status_blocks_acceptance_without_mutating_candidate(self) -> None:
        original = self.candidate.copy()
        with self.assertRaisesRegex(RuntimeError, "status.*verified"):
            self.verify({"data": {"project": {}}})
        self.assertEqual(self.candidate, original)

    def test_public_graphql_status_verifies_archive_and_fork_independently(self) -> None:
        self.assertEqual(self.verify({"data": {"project": {"archived": False,
                                                       "forkedFrom": {"id": "gid://gitlab/Project/1"}}}}), "123")
        self.assertEqual(self.candidate["Archived"], "false")
        self.assertEqual(self.candidate["Fork"], "true")

    def test_graphql_archived_repository_cannot_be_accepted(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "repository is archived"):
            self.verify({"data": {"project": {"archived": True, "forkedFrom": None}}})


if __name__ == "__main__":
    unittest.main()
