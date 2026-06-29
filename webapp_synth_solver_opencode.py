"""Shim so `vf-eval webapp-synth-solver-opencode` resolves.

verifiers resolves an env id by importing `env_id.replace("-", "_")`, i.e.
`webapp_synth_solver_opencode`. This re-exports the real loader.

The webapp solver runs an OpenCode agent in a node-enabled sandbox on a
React/Tailwind task repo, scored by the vitest check harness in-sandbox.
"""

from webapp_synth.env import load_environment

__all__ = ["load_environment"]
