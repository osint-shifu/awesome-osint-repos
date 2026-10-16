from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def step_script(path: Path, name: str) -> str:
    lines = path.read_text().split(f"      - name: {name}\n", 1)[1].splitlines()
    start = lines.index("        run: |") + 1
    script = []
    for line in lines[start:]:
        if line and not line.startswith("          "):
            break
        script.append(line[10:] if line else "")
    return "\n".join(script)


class WorkflowGateTests(unittest.TestCase):
    def run_workflow(self, workflow: str, *, after_rebase: bool, fail_tests: bool = True) -> tuple[int, bool, bool]:
        path = ROOT / ".github/workflows" / workflow
        initial, publish = (
            ("Scan configured public sources", "Commit and publish candidate queue")
            if workflow == "discover.yml"
            else ("Verify catalogue gates", "Commit and publish refreshed metadata")
        )
        script = step_script(path, publish)
        if not after_rebase:
            script = step_script(path, initial) + "\n" + script
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binaries = root / "bin"
            binaries.mkdir()
            (binaries / "git").write_text(
                '#!/bin/bash\n'
                'case "$1" in\n'
                '  diff) [[ " $* " == *" --quiet "* ]] && exit 1; exit 0;;\n'
                '  commit) touch "$TEST_ROOT/committed";;\n'
                '  rebase) touch "$TEST_ROOT/rebased";;\n'
                '  push) touch "$TEST_ROOT/pushed";;\n'
                '  rev-parse) echo aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;;\n'
                '  ls-remote) echo "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa refs/heads/main";;\n'
                'esac\nexit 0\n'
            )
            (binaries / "python").write_text(
                '#!/bin/bash\n'
                'if [[ "$FAIL_TESTS" == 1 && "$1 $2" == "-m unittest" ]]; then\n'
                '  if [[ "$FAIL_AFTER_REBASE" == 0 || -f "$TEST_ROOT/rebased" ]]; then exit 1; fi\n'
                'fi\nexit 0\n'
            )
            for executable in binaries.iterdir():
                executable.chmod(0o755)
            (root / "discovery-report.md").write_text("Discovery report.\n")
            environment = {
                **os.environ, "PATH": str(binaries) + os.pathsep + os.environ["PATH"],
                "TEST_ROOT": str(root), "FAIL_AFTER_REBASE": str(int(after_rebase)),
                "FAIL_TESTS": str(int(fail_tests)),
                "RUNNER_TEMP": str(root), "GITHUB_STEP_SUMMARY": str(root / "summary.md"),
            }
            result = subprocess.run(["/bin/bash", "-c", script], cwd=root, env=environment, capture_output=True)
            return result.returncode, (root / "pushed").exists(), (root / "committed").exists()

    def test_successful_checks_allow_publication_in_both_workflows(self) -> None:
        for workflow in ("discover.yml", "refresh.yml"):
            with self.subTest(workflow=workflow):
                result, pushed, committed = self.run_workflow(workflow, after_rebase=False, fail_tests=False)
                self.assertEqual(result, 0)
                self.assertTrue(committed)
                self.assertTrue(pushed)

    def test_discovery_tests_block_commit(self) -> None:
        result, pushed, committed = self.run_workflow("discover.yml", after_rebase=False)
        self.assertNotEqual(result, 0)
        self.assertFalse(committed)
        self.assertFalse(pushed)

    def test_refresh_tests_block_commit(self) -> None:
        result, pushed, committed = self.run_workflow("refresh.yml", after_rebase=False)
        self.assertNotEqual(result, 0)
        self.assertFalse(committed)
        self.assertFalse(pushed)

    def test_discovery_rebased_tests_block_push(self) -> None:
        result, pushed, committed = self.run_workflow("discover.yml", after_rebase=True)
        self.assertNotEqual(result, 0)
        self.assertTrue(committed)
        self.assertFalse(pushed)

    def test_refresh_rebased_tests_block_push(self) -> None:
        result, pushed, committed = self.run_workflow("refresh.yml", after_rebase=True)
        self.assertNotEqual(result, 0)
        self.assertTrue(committed)
        self.assertFalse(pushed)
