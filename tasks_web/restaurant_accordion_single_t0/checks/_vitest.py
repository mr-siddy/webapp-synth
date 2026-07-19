"""Shared helper: run a vitest spec against a candidate repo and parse results.

Imported by correctness.py and anticheat.py. The check loader puts this file's
directory on sys.path and snapshots sys.modules, so the import is isolated.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

HARNESS_SUBDIR = ".eca_checks"


def _parse_vitest_json(stdout: str) -> tuple[int, int]:
    """Return (passed, total) from vitest's json report (last JSON line wins)."""
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            data = json.loads(line)
        except ValueError:
            continue
        return int(data.get("numPassedTests", 0)), int(data.get("numTotalTests", 0))
    return 0, 0


def run_vitest(repo_path, task_dir, test_file: str) -> tuple[int, int, str]:
    """Copy the harness into <repo>/.eca_checks, npm ci if needed, run one spec.

    Returns (passed, total, tail_of_output). total == 0 signals a harness error.
    """
    repo_path = Path(repo_path)
    harness_src = Path(task_dir) / "checks" / "web"
    dst = repo_path / HARNESS_SUBDIR
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(harness_src, dst)
    report = dst / "report.json"
    try:
        if not (repo_path / "node_modules").is_dir():
            ci = subprocess.run(
                ["npm", "ci"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=600,
            )
            if ci.returncode != 0:
                return 0, 0, f"npm ci failed: {(ci.stdout + ci.stderr)[-400:]}"
        proc = subprocess.run(
            [
                "npx",
                "vitest",
                "run",
                f"{HARNESS_SUBDIR}/{test_file}",
                "--config",
                f"{HARNESS_SUBDIR}/vitest.config.ts",
                "--reporter=json",
                f"--outputFile={HARNESS_SUBDIR}/report.json",
            ],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=600,
        )
        text = report.read_text() if report.is_file() else proc.stdout
        passed, total = _parse_vitest_json(text)
        return passed, total, (proc.stdout + proc.stderr)[-400:]
    finally:
        shutil.rmtree(dst, ignore_errors=True)
