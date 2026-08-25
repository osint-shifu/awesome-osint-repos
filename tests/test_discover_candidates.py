from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / ".catalog" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discover_candidates as discovery


class StrictDiscoveryTests(unittest.TestCase):
    def test_strict_source_error_returns_one_without_writing_candidates(self) -> None:
        source = {"Name": "Broken", "Provider": "Unsupported", "Enabled": "true"}
        with (
            patch.object(
                sys,
                "argv",
                ["discover_candidates.py", "--write", "--fail-on-source-error"],
            ),
            patch.object(discovery, "load_catalog", return_value=([], [])),
            patch.object(
                discovery,
                "load_candidates",
                return_value=(discovery.CANDIDATE_FIELDS, []),
            ),
            patch.object(discovery, "load_sources", return_value=[source]),
            patch.object(discovery, "write_csv") as write_csv,
        ):
            self.assertEqual(discovery.main(), 1)
        write_csv.assert_not_called()

    def test_strict_telegram_lookup_error_is_propagated(self) -> None:
        class FakeClient:
            def get_text(self, url: str) -> str:
                return (
                    '<div class="tgme_widget_message_wrap" data-post="channel/1">'
                    '<time datetime="2026-08-25T00:00:00+00:00"></time>'
                    '<a href="https://github.com/example/tool">tool</a></div>'
                )

        source = {"Query": "https://t.me/s/channel"}
        with patch.object(
            discovery,
            "repository_item",
            side_effect=RuntimeError("timeout"),
        ):
            with self.assertRaisesRegex(RuntimeError, "Telegram repository lookup failed"):
                discovery.telegram_items(FakeClient(), source, "2026-08-25", 10, True)


if __name__ == "__main__":
    unittest.main()
