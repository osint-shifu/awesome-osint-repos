from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_changed_files


class ChangedFileTests(unittest.TestCase):
    def test_allows_only_candidate_csv(self) -> None:
        self.assertEqual(
            check_changed_files.unexpected_paths(
                [".catalog/data/candidates.csv"],
                [".catalog/data/candidates.csv"],
            ),
            [],
        )

    def test_reports_unique_sorted_disallowed_paths(self) -> None:
        self.assertEqual(
            check_changed_files.unexpected_paths(
                ["README.md", ".catalog/data/candidates.csv", "README.md", "AGENTIC.md"],
                [".catalog/data/candidates.csv"],
            ),
            ["AGENTIC.md", "README.md"],
        )


if __name__ == "__main__":
    unittest.main()
