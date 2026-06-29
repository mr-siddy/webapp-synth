"""FrontendHarnessTaskSet — React/Tailwind tasks from tasks_web/, scored in a node sandbox.

Cross-repo note: this package (webapp_synth) is separate from evolving-coding-agent,
which it depends on. The sandbox needs BOTH the evolving_coding_agent package source
(for the `evolving-coding-agent` score CLI it runs in-sandbox) AND this repo's task.
So `setup` stages the package from the installed evolving_coding_agent location and
the task from this repo's tasks_web/, into a single `tasks/<name>` sandbox layout.
"""

from __future__ import annotations

import asyncio
import shutil
import tempfile
from pathlib import Path

import evolving_coding_agent
import verifiers as vf
from verifiers.envs.experimental.composable import SandboxSpec

from evolving_coding_agent.solver.taskset import HarnessTaskSet, _tar_staged_package
from evolving_coding_agent.utils import _SOLVER_STAGE_INCLUDE, _SOLVER_TASK_EXCLUDE

# Roots: this repo (for tasks_web/) and the evolving_coding_agent package (for the
# package source we install in the sandbox). EVOLVE_CC_ROOT is derived from the
# installed package so it works regardless of the sibling-directory layout.
WEBAPP_ROOT = Path(__file__).resolve().parents[1]
TASKS_WEB_DIR = WEBAPP_ROOT / "tasks_web"
EVOLVE_CC_ROOT = Path(evolving_coding_agent.__file__).resolve().parents[1]


class FrontendHarnessTaskSet(HarnessTaskSet):
    """Loads frontend tasks from tasks_web/ and provisions a node-capable sandbox."""

    # Read tasks from tasks_web/ but keep the sandbox layout at tasks/<name>.
    source_tasks_subdir = "tasks_web"

    def __init__(self, tasks_dir: Path = TASKS_WEB_DIR, **kwargs):
        super().__init__(tasks_dir=tasks_dir, **kwargs)

    def get_sandbox_spec(self, info) -> SandboxSpec:
        # Bump memory/disk over the base python spec for npm install + vitest.
        return SandboxSpec(
            image="python:3.11-slim",
            cpu_cores=2,
            memory_gb=4,
            disk_size_gb=8,
            timeout_minutes=120,
        )

    def get_rubric(self):
        from .rubric import FrontendRubric

        return FrontendRubric()

    def _stage_cross_repo(self, task_name: str) -> Path:
        """Stage evolving_coding_agent (from EVOLVE_CC_ROOT) + the task (from this
        repo's tasks_web/) into one staging dir laid out as tasks/<name>."""
        staging = Path(tempfile.mkdtemp(prefix="ga-webapp-upload-"))
        for name in _SOLVER_STAGE_INCLUDE:  # evolving_coding_agent + shims + pyproject
            src = EVOLVE_CC_ROOT / name
            if not src.exists():
                continue
            dest = staging / name
            if src.is_dir():
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy2(src, dest)
        if task_name:
            task_src = TASKS_WEB_DIR / task_name
            if task_src.is_dir():
                shutil.copytree(
                    task_src,
                    staging / "tasks" / task_name,  # sandbox layout is always tasks/<name>
                    ignore=shutil.ignore_patterns(*_SOLVER_TASK_EXCLUDE),
                )
        return staging

    async def setup(self, state) -> None:
        """Cross-repo stage + upload, fresh per rollout (race-safe via the client)."""
        info = state.get("info") or {}
        task_name = info.get("task_name", "")

        staged = await asyncio.to_thread(self._stage_cross_repo, task_name)
        try:
            tar_path = await asyncio.to_thread(_tar_staged_package, staged)
            try:
                sandbox_id = state["sandbox_id"]
                client = state["sandbox_client"]
                remote_tar = "/tmp/evolving_coding_agent_package.tar.gz"
                await client.upload_file(sandbox_id, remote_tar, str(tar_path))
                result = await client.execute_command(
                    sandbox_id,
                    f"mkdir -p /workspace && tar -xzf {remote_tar} -C / && rm {remote_tar} && "
                    f"echo '{task_name}' > /workspace/.task_name",
                    timeout=60,
                )
                if result.exit_code != 0:
                    output = (result.stdout or "") + (result.stderr or "")
                    raise vf.SandboxError(
                        f"Package upload extract failed (exit={result.exit_code}): {output[:500]}"
                    )
            finally:
                tar_path.unlink(missing_ok=True)
        finally:
            await asyncio.to_thread(shutil.rmtree, staged, ignore_errors=True)
