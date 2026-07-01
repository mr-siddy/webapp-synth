"""OpenCode harness for React/Tailwind tasks: base opencode + python + Node LTS.

Reuses the maintained opencode repo harness from evolving-coding-agent (correct
XDG config, small-model pin, editable package install) and appends a pinned Node
install so the vitest check harness can run in the sandbox. Node lives under
~/.local/node; the rubric prepends ~/.local/node/bin to PATH when it scores.
"""

from __future__ import annotations

from verifiers.envs.experimental.composable import Harness

from evolving_coding_agent.solver.opencode.harness import opencode_repo_harness

NODE_VERSION = "v20.18.0"
NODE_INSTALL_SCRIPT = f"""
# Node LTS for the vitest check harness (pinned for reproducibility)
NODE_VER={NODE_VERSION}
curl -fsSL https://nodejs.org/dist/$NODE_VER/node-$NODE_VER-linux-x64.tar.xz -o /tmp/node.tar.xz
mkdir -p $HOME/.local/node
tar -xf /tmp/node.tar.xz -C $HOME/.local/node --strip-components=1
rm -f /tmp/node.tar.xz
export PATH="$HOME/.local/node/bin:$PATH"
node --version
npm --version

# Best-effort: pre-install the task repo's deps during setup (the network-open
# phase) so check() execution is offline and fast. If the workdir isn't set yet,
# the check-time `npm ci` fallback in checks/_vitest.py still handles it.
if [ -n "$AGENT_WORKDIR" ] && [ -f "$AGENT_WORKDIR/package.json" ]; then
  (cd "$AGENT_WORKDIR" && npm ci --no-audit --no-fund 2>&1 | tail -3) || echo "npm ci deferred to check-time"
fi
"""


def frontend_repo_harness() -> Harness:
    """OpenCode harness with the evolving-coding-agent install + a pinned Node LTS."""
    harness = opencode_repo_harness()
    harness.install_script = (harness.install_script or "") + NODE_INSTALL_SCRIPT
    return harness
