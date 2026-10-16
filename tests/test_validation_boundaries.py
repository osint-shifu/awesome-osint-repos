from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".catalog/scripts"))
import catalog_common as common
import validate_catalog as validator
from tests.test_metadata_updates import catalogue_row


class ValidationBoundaryTests(unittest.TestCase):
    def validate_row(self, field: str, value: str):
        row = catalogue_row()
        row[field] = value
        result = validator.Validation()
        with patch.object(validator, "load_catalog", return_value=(common.ALL_COLUMNS, [row])):
            validator.validate_catalog(result)
        return result.errors

    def test_impossible_calendar_date_is_rejected(self) -> None:
        self.assertTrue(any("Created" in error for error in self.validate_row("Created", "2026-02-30")))

    def test_negative_star_count_is_rejected(self) -> None:
        self.assertTrue(any("Stars" in error for error in self.validate_row("Stars", "-1")))

    def test_invalid_addition_date_does_not_crash_marker_generation(self) -> None:
        row = {"Repository": "https://github.com/example/tool", "Added": "2026-02-30"}
        try:
            result = common.recent_repository_keys([row], "2026-03-01")
        except ValueError:
            result = {"invalid date accepted"}
        self.assertEqual(result, set())
