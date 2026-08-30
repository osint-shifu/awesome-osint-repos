from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import catalog_common


def row(project: str, platform: str, stars: str = "0") -> dict[str, str]:
    return {
        "Project": project,
        "Categories": "Social Media",
        "Platform": platform,
        "Stars": stars,
        "Review Status": "accepted",
    }


class PlatformVocabularyTests(unittest.TestCase):
    def test_platform_column_is_appended_last(self) -> None:
        self.assertEqual(catalog_common.ALL_COLUMNS[-1], "Platform")

    def test_appending_leaves_every_earlier_column_index_unchanged(self) -> None:
        previous = [
            "Project", "Repository", "Description", "Target Input", "Categories",
            "Type", "AI Agent", "License", "Stars", "Created", "Last Update", "Added",
            "Verified", "Hosting", "Repository ID", "Archived", "Fork",
            "Repository Status", "Review Status", "Discovery Source", "Source Files",
        ]
        self.assertEqual(catalog_common.ALL_COLUMNS[: len(previous)], previous)

    def test_canonical_platform_accepts_known_value(self) -> None:
        self.assertEqual(catalog_common.canonical_platform("Telegram"), "Telegram")

    def test_canonical_platform_accepts_blank(self) -> None:
        self.assertEqual(catalog_common.canonical_platform(""), "")

    def test_canonical_platform_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            catalog_common.canonical_platform("Twitter")


class PlatformGroupTests(unittest.TestCase):
    def test_cross_platform_group_comes_first(self) -> None:
        groups = catalog_common.platform_groups(
            [row("Sherlock", ""), row("Tosint", "Telegram")]
        )
        self.assertEqual([label for label, _ in groups], ["Cross-platform", "Telegram"])

    def test_platforms_are_ordered_by_row_count_descending(self) -> None:
        rows = [
            row("a", "Instagram"), row("b", "Instagram"), row("c", "Instagram"),
            row("d", "Telegram"), row("e", "Telegram"),
            row("f", "Reddit"),
        ]
        self.assertEqual(
            [label for label, _ in catalog_common.platform_groups(rows)],
            ["Instagram", "Telegram", "Reddit"],
        )

    def test_equal_counts_break_alphabetically(self) -> None:
        rows = [row("a", "Telegram"), row("b", "Instagram")]
        self.assertEqual(
            [label for label, _ in catalog_common.platform_groups(rows)],
            ["Instagram", "Telegram"],
        )

    def test_platform_without_rows_produces_no_group(self) -> None:
        labels = [label for label, _ in catalog_common.platform_groups([row("a", "Reddit")])]
        self.assertEqual(labels, ["Reddit"])
        self.assertNotIn("Snapchat", labels)

    def test_group_rows_keep_star_descending_order(self) -> None:
        rows = [row("small", "Telegram", "5"), row("big", "Telegram", "900")]
        _, grouped = catalog_common.platform_groups(rows)[0]
        self.assertEqual([item["Project"] for item in grouped], ["big", "small"])

    def test_empty_input_produces_no_groups(self) -> None:
        self.assertEqual(catalog_common.platform_groups([]), [])


class PlatformValidationTests(unittest.TestCase):
    """The validator rules, exercised through the pure helper they call."""

    def test_platform_outside_social_media_is_a_violation(self) -> None:
        offender = {"Categories": "Geolocation", "Platform": "Telegram"}
        self.assertTrue(catalog_common.misplaced_platform(offender))

    def test_platform_inside_social_media_is_allowed(self) -> None:
        allowed = {"Categories": "Social Media", "Platform": "Telegram"}
        self.assertFalse(catalog_common.misplaced_platform(allowed))

    def test_blank_platform_outside_social_media_is_allowed(self) -> None:
        allowed = {"Categories": "Geolocation", "Platform": ""}
        self.assertFalse(catalog_common.misplaced_platform(allowed))

    def test_blank_platform_inside_social_media_is_allowed(self) -> None:
        allowed = {"Categories": "Social Media", "Platform": ""}
        self.assertFalse(catalog_common.misplaced_platform(allowed))
