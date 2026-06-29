"""FrontendRubric — score React/Tailwind rollouts inside the node sandbox.

Always scores in-sandbox: re-upload the stripped checks/ + task.toml, run the
`evolving-coding-agent score` CLI there (node + npm + vitest available), parse the
JSON. No pip extra_deps; the reference repo is omitted (SP1 bakes expected values
into the spec). graded_reward / CheckOutcome are reused verbatim from the base.
"""

from __future__ import annotations

import json
import shlex
import shutil
from pathlib import Path

from evolving_coding_agent.solver.rubric import (
    FINAL_REPO_PATH,
    SANDBOX_TASK_DIR,
    SANDBOX_TASKS_BASE,
    HarnessRubric,
    _tar_dir,
)
from evolving_coding_agent.taskset import CheckOutcome, load_check_specs

NODE_PATH_EXPORT = 'export PATH="$HOME/.local/node/bin:$HOME/.local/bin:$PATH";'


class FrontendRubric(HarnessRubric):
    """Score sandbox rollouts by running the vitest harness in-sandbox."""

    async def _check_results(self, state) -> dict[str, CheckOutcome]:
        if "check_results" in state:
            return state["check_results"]
        info = state.get("info") or {}
        results = await self._score_in_sandbox_frontend(state, info)
        state["check_results"] = results
        return results

    async def _score_in_sandbox_frontend(self, state, info) -> dict[str, CheckOutcome]:
        task_name = info.get("task_name", "")
        sandbox_id = state.get("sandbox_id")
        client = state.get("sandbox_client")

        def _fail(msg: str) -> dict[str, CheckOutcome]:
            return {
                name: CheckOutcome(name=name, score=0.0, passed=False, message=msg)
                for name in load_check_specs(info)
            }

        if not task_name or not sandbox_id or not client:
            return _fail("frontend task requires a sandbox to score (use the webapp solver)")

        local_task_dir = Path(info["task_dir"])
        checks_dir = local_task_dir / "checks"
        task_toml = local_task_dir / "task.toml"
        remote_task_dir = SANDBOX_TASK_DIR.format(task_name=task_name)
        uploads: list[Path] = []
        try:
            # 1. Re-upload the stripped scoring artifacts the agent never saw.
            if not checks_dir.is_dir() or not task_toml.is_file():
                return _fail("missing local scoring artifacts (checks/ or task.toml)")
            checks_tar = _tar_dir(checks_dir, "checks")
            uploads.append(checks_tar.parent)
            remote_checks_tar = f"/tmp/{task_name}_checks.tar.gz"
            await client.upload_file(sandbox_id, remote_checks_tar, str(checks_tar))
            r = await client.execute_command(
                sandbox_id,
                f"tar -xzf {remote_checks_tar} -C {remote_task_dir} && rm -f {remote_checks_tar}",
                timeout=60,
            )
            if r.exit_code != 0:
                return _fail(f"failed to upload checks: {(r.stdout or '') + (r.stderr or '')}"[:300])
            await client.upload_file(
                sandbox_id, f"{remote_task_dir}/task.toml", str(task_toml)
            )

            # 2. Score in-sandbox (node on PATH; no --reference-repo for SP1).
            candidate = FINAL_REPO_PATH.format(task_name=task_name)
            r = await client.execute_command(
                sandbox_id,
                f"{NODE_PATH_EXPORT} cd /workspace/evolving-coding-agent && "
                f"evolving-coding-agent score {shlex.quote(task_name)} "
                f"--tasks-dir {shlex.quote(SANDBOX_TASKS_BASE)} "
                f"--candidate-repo {shlex.quote(candidate)}",
                timeout=900,
            )
            out = (r.stdout or "").strip()
            payload = {}
            for line in reversed(out.splitlines()):
                line = line.strip()
                if line.startswith("{"):
                    try:
                        payload = json.loads(line)
                        break
                    except ValueError:
                        continue
            if not payload:
                return _fail(f"could not parse sandbox score output: {out[-400:]}")
            checks = payload.get("checks") or {}
            if not checks:
                return _fail(f"sandbox score returned no checks: {payload}")
            return {
                name: CheckOutcome(
                    name=name,
                    score=float(checks.get(name, {}).get("score", 0.0)),
                    passed=bool(checks.get(name, {}).get("passed", False)),
                    message=str(checks.get(name, {}).get("message", "")),
                )
                for name in checks
            }
        finally:
            for d in uploads:
                shutil.rmtree(d, ignore_errors=True)
