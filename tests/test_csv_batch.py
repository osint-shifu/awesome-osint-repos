from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".catalog/scripts"))
from catalog_common import write_csv, write_csv_batch


class CSVBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.first = self.root / "first.csv"
        self.second = self.root / "second.csv"
        write_csv(self.first, ["Value"], [{"Value": "old first"}])
        write_csv(self.second, ["Value"], [{"Value": "old second"}])

    def test_preparation_failure_does_not_replace_any_destination(self) -> None:
        original = self.first.read_bytes(), self.second.read_bytes()
        def broken_rows():
            yield {"Value": "partial"}
            raise ValueError("input failed")
        with self.assertRaises(ValueError):
            write_csv_batch([
                (self.first, ["Value"], [{"Value": "new first"}]),
                (self.second, ["Value"], broken_rows()),
            ])
        self.assertEqual((self.first.read_bytes(), self.second.read_bytes()), original)
        self.assertEqual(sorted(path.name for path in self.root.iterdir()), ["first.csv", "second.csv"])

    def test_rollback_removes_a_destination_that_did_not_previously_exist(self) -> None:
        self.first.unlink()
        original = self.second.read_bytes()
        replace = Path.replace
        def fail(path, target):
            if Path(target) == self.second:
                raise OSError("publish failed")
            return replace(path, target)
        with patch.object(Path, "replace", fail), self.assertRaises(OSError):
            write_csv_batch([
                (self.first, ["Value"], [{"Value": "new first"}]),
                (self.second, ["Value"], [{"Value": "new second"}]),
            ])
        self.assertFalse(self.first.exists())
        self.assertEqual(self.second.read_bytes(), original)

    def test_failed_rollback_retains_the_original_for_recovery(self) -> None:
        original = self.first.read_bytes()
        replace = Path.replace
        def fail(path, target):
            if Path(target) == self.second or path.name == "previous.csv":
                raise OSError("destination unavailable")
            return replace(path, target)
        with patch.object(Path, "replace", fail), self.assertRaisesRegex(OSError, "Recovery files retained"):
            write_csv_batch([
                (self.first, ["Value"], [{"Value": "new first"}]),
                (self.second, ["Value"], [{"Value": "new second"}]),
            ])
        backups = list(self.root.glob(".first.csv-*/previous.csv"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), original)
