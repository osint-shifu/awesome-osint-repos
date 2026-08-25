#!/usr/bin/env python3
"""Reject tracked working-tree paths outside an explicit allowlist."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Iterable


def unexpected_paths(paths: Iterable[str], allowed_paths: Iterable[str]) -> list[str]:
    allowed = set(allowed_paths)
    return sorted({path for path in paths if path and path not in allowed})


def changed_paths(base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--no-renames", "--name-only", base],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--allow", action="append", required=True)
    args = parser.parse_args()
    violations = unexpected_paths(changed_paths(args.base), args.allow)
    if not violations:
        return 0
    print("Unexpected tracked changes:", file=sys.stderr)
    print("\n".join(violations), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
