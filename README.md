# webapp-synth

Synthetic-data generation for React/Tailwind landing-page coding tasks.

This is a standalone repo that **reuses** the scoring engine of
[`evolving-coding-agent`](../evolve-cc) by depending on it (editable, from the
local `../evolve-cc` checkout). It contains only the new, frontend-specific code:

- `webapp_synth/` — the solver module (node-enabled sandbox harness, taskset,
  rubric, env) that subclasses evolving-coding-agent's opencode solver classes.
- `tasks_web/` — the React/Tailwind landing-page task corpus.
- `docs/` — design spec and implementation plan.

## Setup
```bash
uv venv
uv pip install -e ../evolve-cc      # the dependency (editable), brings verifiers/tyro/etc.
uv pip install -e . --no-deps       # this package
uv run pytest                       # (once tests exist)
```
