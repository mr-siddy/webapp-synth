"""Webapp solver env (`vf-eval webapp-synth-solver-opencode`).

Runs an OpenCode agent in a node-enabled Prime sandbox on a React/Tailwind task
repo, scored by the vitest check harness in-sandbox. Reuses evolving-coding-agent's
ComposableEnv wiring; only the taskset (tasks_web + node sandbox + cross-repo
staging), harness (node provisioning), and rubric (in-sandbox vitest scoring) differ.
"""

from __future__ import annotations

from pathlib import Path

import verifiers as vf
from verifiers.envs.experimental.composable import ComposableEnv

from .harness import frontend_repo_harness
from .taskset import TASKS_WEB_DIR, FrontendHarnessTaskSet


def load_environment(
    tasks_dir: str | Path = TASKS_WEB_DIR,
    task: str | None = None,
    min_tier: int | None = None,
    max_tier: int | None = None,
    min_pass_rate: float = 0.0,
    max_pass_rate: float = 1.0,
    pass_rate_key: tuple[str, str] = ("Qwen/Qwen3.5-4B", "webapp-opencode"),
    max_turns: int = 100,
    timeout_seconds: float = 3600.0,
    sandbox_labels: list[str] | None = None,
    **kwargs,
) -> vf.Environment:
    taskset = FrontendHarnessTaskSet(
        tasks_dir=Path(tasks_dir),
        task=task,
        min_tier=min_tier,
        max_tier=max_tier,
        min_pass_rate=min_pass_rate,
        max_pass_rate=max_pass_rate,
        pass_rate_key=pass_rate_key,
    )
    harness = frontend_repo_harness()
    return ComposableEnv(
        taskset=taskset,
        harness=harness,
        keep_sandbox_for_scoring=True,
        max_turns=max_turns,
        timeout_seconds=timeout_seconds,
        labels=sandbox_labels if sandbox_labels is not None else ["webapp-synth"],
        **kwargs,
    )
