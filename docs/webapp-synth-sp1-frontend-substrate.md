# SP1 — Frontend Task Substrate (vertical slice)

- **Date:** 2026-06-28
- **Status:** Approved design, ready for implementation planning
- **Topic:** Repointing the synthetic-data pipeline toward webapps / landing pages — first sub-project (SP1) of the larger "webapp synthesis" pivot.

---

## 1. Context & motivation

`evolve-cc` today is a self-growing coding-task environment for repo-editing RL
agents. The synthesizer (Claude Code + the `synthesize-task` skill) authors
Python bug-repair task families; the solver (a `verifiers` environment) runs a
small student model against repo-editing tools and scores it with a deterministic,
cheat-safe reward (`graded_reward` in `evolving_coding_agent/taskset.py`):
`reward = mean(functional checks) if all anti-cheat gates pass else 0.0`.

We are pivoting the synthetic-data target to **generating webapps / landing pages
across industry verticals**. The chosen data shape is **hybrid**: a finished
landing page is the keystone artifact that serves both as (a) an SFT target
(industry brief → finished page) and (b) the "solved" reference from which we
derive repair/implement RL tasks (the broken→finished diff becomes the
`finalize`-generated reference patch; the finished page is the differential
reference the checks compare against).

This is four independent subsystems, decomposed as:

- **SP1 — Frontend task substrate (this spec).** The scoring/rendering foundation,
  proven end-to-end on one hand-authored reference page + one derived repair task.
  Everything else depends on it.
- **SP2 — Industry taxonomy.** Industries × page archetypes × required
  sections/components/interactions (the new "domain library").
- **SP3 — Page generator + quality judge + SFT pairs.** Generate finished pages,
  LLM/vision judge for best-of-N selection, emit SFT data.
- **SP4 — Task-derivation pipeline at scale.** Systematically break/stub finished
  pages into a full t0–t4 tier ladder; calibrate bands via pass-rate.

### Decisions locked during brainstorming

1. **Data shape:** Hybrid (SFT pairs + derived RL repair/implement tasks). SP1
   covers only the RL conformance substrate; generation is SP3.
2. **Stack:** React + Tailwind (modern, production-like). Build tool: **Vite +
   React + TypeScript + Tailwind** (SPA single landing page). Not Next.js — no
   SSR/server-component complexity is needed for a landing page, and Vite is the
   lightest realistic modern stack.
3. **Scoring:** **Split.** Deterministic rendered-DOM/behavior conformance is the
   RL **reward** (reproducible, cheat-safe, band-gateable). A separate LLM/vision
   quality judge ranks pages for the **SFT** half only (SP3, out of scope here).
4. **Render engine:** **Vitest + React Testing Library + jsdom.** Asserts
   roles/headings/text/links/alt-text/form-fields and behavior (via `user-event`),
   plus responsive-*class* presence (e.g. `md:grid-cols-3`). No browser binaries;
   fast; deterministic. True computed layout / pixels are deferred to Playwright
   in SP3.
5. **Structure:** **Parallel track.** A new `tasks_web/` corpus dir, new webapp env
   entry points, and a new `evolving_coding_agent/frontend/` module that *reuses*
   the core scoring engine. The existing 868-task Python corpus, its envs, and the
   fast local gate are untouched.
6. **Where it runs:** Frontend tasks are **sandbox-native** — solved and scored in
   the opencode sandbox with a node toolchain added. The fast in-process local
   gate does not apply to webapp tasks.

---

## 2. Scope

SP1 validates the substrate; it does **not** calibrate difficulty or scale.

**In scope**

- The on-disk frontend task format (`tasks_web/<name>/`).
- A node-enabled sandbox spec + node provisioning.
- The vitest/jsdom check harness invoked from Python `check()` wrappers.
- A `FrontendHarnessTaskSet` + `FrontendRubric` that score in-sandbox, reusing the
  core engine.
- New webapp env entry points + top-level shim.
- One concrete vertical-slice family: one hand-authored React/Tailwind reference
  page + one derived repair task at t0, taken through `finalize → validate →
  measure`.
- The minimal core tweaks needed to let a non-Python repo flow through existing
  helpers.

**Out of scope (later sub-projects)**

- The page generator, SFT pairs, and the LLM/vision quality judge (SP3).
- The industry taxonomy / domain library (SP2).
- The full t0–t4 tier ladder and corpus scaling (SP4).
- Playwright / real-browser / visual / true-layout assertions.
- A prebuilt custom sandbox image (runtime node install is fine for SP1).

---

## 3. The vertical-slice family (concrete)

- **Industry / page:** a SaaS project-management product landing page, codenamed
  **"TaskFlow"** — a single landing page composed of: a sticky top nav, a hero
  (headline + subhead + primary CTA), a 3-card features grid, a 3-tier pricing
  section with a "Most popular" highlight, an FAQ accordion, a footer, and a
  mobile hamburger menu. This mix exercises structure, behavior, and
  responsive-class assertions. The industry is swappable; it is only the slice.
- **The reference (solved) page** is hand-authored and lives *outside* the task
  tree, in a scratch fixed-repo (e.g. `/tmp/cc-synth/fixed_repos/taskflow_repair_t0/`),
  exactly like the current synthesis flow.
- **The one repair defect (t0):** the mobile hamburger menu does not close after a
  nav link is tapped (missing close-on-navigate). The `instruction.md` is
  **symptom-only**: "On a phone, tapping an item in the menu jumps to the right
  section but the menu stays open, covering the page; it should close once a
  destination is chosen." It never names the component, file, handler, or fix.
- One clean, observable defect is deliberate: SP1 proves the loop, not difficulty.

---

## 4. Frontend task format

```
tasks_web/taskflow_repair_t0/
├── instruction.md          # symptom-only (unchanged contract)
├── repo/                   # a real Vite + React + TS + Tailwind project (committed, unsolved)
│   ├── package.json
│   ├── package-lock.json   # committed, PINNED deps — determinism
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       └── components/{Nav,Hero,Features,Pricing,FAQ,Footer,MobileMenu}.tsx
├── reference.patch         # finalize-generated, NEVER hand-written (unchanged)
├── checks/
│   ├── correctness.py      # Python wrapper → runs vitest, parses JSON → continuous score
│   ├── anticheat.py        # Python wrapper → static guards + vitest gate → binary
│   └── web/                # vitest harness (NOT shipped to the solver)
│       ├── vitest.config.ts
│       ├── setup.ts        # jsdom env, mocks fetch, pins Date/Math.random
│       ├── correctness.test.tsx
│       └── anticheat.test.tsx
└── task.toml
```

`repo/` is committed **without** `node_modules/` or `dist/` (never built before
commit). `checks/` (including `checks/web/`) is private and stripped from the
solver staging, like every other task's `checks/`.

### `task.toml` additions

The schema is unchanged except for one marker that routes scoring to the sandbox:

```toml
[metadata]
name = "taskflow_repair_t0"
description = "..."
tier = 0
parent = ""
domain = "taskflow"
archetype = "repair"
kind = "frontend"                 # NEW: routes to the node sandbox + vitest harness
repo_path = "repo"
reference_patch = "reference.patch"
evolution_strategies = []

[[metadata.pass_rates]]
solver = "webapp-opencode"        # the new sandbox solver key
model = "<student_model>"
k = 10
value = 0.0                       # placeholder until measured
measured = false
in_band = false
attempts = 0

[checks]
correctness = "checks/correctness.py"
anticheat = "checks/anticheat.py"
```

`kind = "frontend"` is the single new field. It plays the same routing role that
`extra_deps` plays for Path-A Python tasks today: its presence means "this task
cannot be scored in-process; it needs the node sandbox." The `[checks]` table and
`[[metadata.pass_rates]]` schema are otherwise identical, so all existing metadata
helpers (`parse_pass_rates`, `matches_pass_rate`) work unchanged.

---

## 5. Check harness

Both check files keep the existing contract —
`def check(repo_path, task_dir, reference_repo_path=None) -> bool | float | dict` —
so `_normalize_check_result`, `run_check_file` (with its determinism guard and
`sys.modules`/`sys.path` snapshotting), `run_check_ensemble`, and `graded_reward`
are reused **verbatim**. The Python check is a thin wrapper that shells out to
node.

### `correctness.py` (functional, continuous)

1. `npm ci` in `repo_path` (from the committed `package-lock.json` → reproducible
   install). Cached across checks within one rollout where possible.
2. `npx vitest run --reporter=json` against `checks/web/correctness.test.tsx`.
3. Parse the JSON reporter output → `score = passed_assertions / total_assertions`,
   `passed = (passed == total)`. Return
   `{"score": passed/total, "passed": passed == total, "message": "..."}`.

The **many seeded sub-cases** the difficulty model wants are individual RTL
assertions inside `correctness.test.tsx`: presence/roles of each required section,
heading text, nav anchors wired to section ids, image alt text, pricing tiers and
the "Most popular" badge, FAQ items, responsive classes (e.g. the features grid
carries `grid-cols-1 md:grid-cols-3`), and **behavior** via `@testing-library/user-event`
(open the mobile menu → click a link → assert the menu is no longer in the
document). Continuous `score` gives `mean@k` the resolution to land in a band.

### `anticheat.py` (binary gate)

- **Static guards** (string/AST-ish over `repo/src`): required components/sections
  not deleted, no large hardcoded text dump substituted for real markup, no
  targeting of check-only test ids / no test-specific shortcut branches.
- A small **vitest anticheat suite** (`anticheat.test.tsx`) for behavioral
  cheat-resistance where static analysis is insufficient.
- Returns `{"passed": bool, "message": "..."}` — unchanged reward semantics
  (`anticheat` is in `ANTI_CHEAT_NAMES`, so it is recognized as the gate by name).

### Determinism

- Committed `package-lock.json` + `npm ci` pins the dependency graph.
- `checks/web/setup.ts` runs in jsdom, **mocks `fetch`** (a landing-page contact
  form must be asserted on client behavior, never a real request), and pins
  `Date` / `Math.random` (the Python network guard does not reach node's separate
  subprocess, so JS-side mocking is **mandatory**).
- Assertions never depend on animation/transition timing.

### Differential vs reference (SP1 simplification)

`reference_repo_path` stays in the `check()` signature for future use, but in SP1
the expected values are **baked into the spec** from the known hand-authored
reference, rather than building and rendering the reference repo a second time per
check (which would double npm-install + vitest cost). Building/rendering the
reference for a true differential is deferred to SP4.

---

## 6. Sandbox + solver + scoring integration

A new `evolving_coding_agent/frontend/` module, built by subclassing the existing
opencode solver classes so the sandbox lifecycle, staging, and in-sandbox scoring
pattern are reused.

- **`FrontendHarnessTaskSet(HarnessTaskSet)`** (`frontend/taskset.py`)
  - `_build_dataset` loads from `tasks_web/` and includes only `kind == "frontend"`
    tasks (same loader shape as `HarnessTaskSet._build_dataset`).
  - `get_sandbox_spec` → node-enabled `SandboxSpec`: keep `python:3.11-slim` as the
    base but bump resources (≈ `memory_gb=4`, `disk_size_gb=8`) for `npm install` +
    vitest; node itself is installed at runtime (below).
  - `get_workdir` → the task's `repo/` (the agent edits it), exactly as today.
  - `setup` reuses the per-rollout stage-and-upload via `state["sandbox_client"]`
    (the race-safe pattern already in `HarnessTaskSet.setup`); staging strips
    `checks/` via the existing `_SOLVER_TASK_EXCLUDE` list in `utils.py`.
- **Node provisioning** via the harness `install_script` (`frontend/harness.py`),
  reusing the existing append pattern in `opencode/harness.py` that already
  installs `uv` + `uv pip install --system -e .`. Append a step that installs a
  pinned **Node LTS** (download the official tarball to `$HOME/.local`, add to
  `PATH`) so the python CLI *and* node coexist. (A prebuilt node+python image is a
  later optimization, not SP1.) Network during sandbox *setup* is unrestricted —
  the determinism guard only applies inside `check()` execution.
- **`FrontendRubric(HarnessRubric)`** (`frontend/rubric.py`)
  - Overrides `_check_results` to always take the **in-sandbox** scoring route
    (the same shape as `HarnessRubric._score_in_sandbox` used for Path-A today):
    re-upload the stripped `checks/` + `task.toml`, run the vitest harness inside
    the sandbox against the agent's final `repo/`, read back JSON, and map to
    `CheckOutcome`s. `graded_reward` / `CheckOutcome` are reused verbatim.
  - Reuses `@vf.cleanup cleanup_sandbox`.
- **Env wiring** (`frontend/env.py` + top-level shim
  `evolving_coding_agent_webapp_solver_opencode.py`): `load_environment` builds
  `ComposableEnv(taskset=FrontendHarnessTaskSet(...), harness=frontend_harness(),
  keep_sandbox_for_scoring=True, ...)`, mirroring `solver/opencode/env.py`.
- **`pyproject.toml`**: add an entry point under
  `[project.entry-points."verifiers.envs"]`:
  `evolving-coding-agent-webapp-solver-opencode =
  "evolving_coding_agent.frontend.env:load_environment"`, and add the shim to the
  wheel `packages` list + `tasks_web` to packaged data.
- **Pass-rate gate:** for frontend tasks the 10-rollout gate runs through this
  sandbox env (slower than the local gate — minutes per measurement — which is
  expected and acceptable). The `pass_rates` solver key is `"webapp-opencode"`.

---

## 7. Reuse map

**Reused verbatim (no change):**

- `graded_reward`, `CheckOutcome`, `_normalize_check_result`
- `run_check_file` + `deterministic_check_env` + `run_check_ensemble`
- `generate_reference_patch_from_repos`, `apply_reference_patch`,
  `prepare_reference_repo`
- The `validate_instance` RED→GREEN admission flow
- The `[checks]` name-convention scoring (`ANTI_CHEAT_NAMES`)
- Pass-rate metadata helpers (`parse_pass_rates`, `matches_pass_rate`,
  `format_pass_rate`)
- The opencode sandbox lifecycle + race-safe per-rollout staging
  (`stage_package_for_solver`, `_SOLVER_TASK_EXCLUDE`)

**New code:**

- `evolving_coding_agent/frontend/{__init__,taskset,rubric,harness,env}.py`
- The vitest check-harness scaffold under each task's `checks/web/`
- The node-enabled `SandboxSpec`
- Env entry point + top-level shim `evolving_coding_agent_webapp_solver_opencode.py`
- The `tasks_web/` corpus dir + the one vertical-slice family
- A forked/extended `synthesize-webapp-task` skill (synth half — minimal for SP1)

**Small core tweaks (carefully scoped, must not regress the Python corpus):**

- `make_repo_copy` / `is_repo_visible_file` (and `CACHE_DIR_NAMES`) must ignore
  `node_modules/`, `dist/`, `.vite/` so copies/patches/listings never include build
  output.
- `finalize` / `validate` / `score` run the vitest harness for `kind == "frontend"`
  tasks, which requires **node on the host** wherever they run (the synth/CI box) —
  analogous to today's `--install-deps` precondition for Path-A. Document this; gate
  with a clear error if node is absent.
- `validate_task_imports` already only scans `.py` files, so a `.tsx` repo passes
  it unchanged; no change needed there.

---

## 8. Determinism, risks, mitigations

| Risk | Mitigation |
|------|------------|
| `npm install` nondeterminism | Commit `package-lock.json`; use `npm ci` (lockfile-exact, no resolution). |
| Per-rollout cost (install + vitest) | jsdom (no browser binaries); `npm ci` + vitest ≈ 30–60s; acceptable for a sandbox gate. |
| JS-side network/time flakiness | Mock `fetch`, pin `Date`/`Math.random` in `setup.ts` (Python guard can't reach node). |
| jsdom can't compute layout | Verify "responsive" via Tailwind class presence; true layout deferred to Playwright/SP3. |
| Node missing on synth/CI host for `validate`/`finalize` | Documented prerequisite; fail fast with a clear message. |
| Sandbox memory pressure (npm + vite) | Bump sandbox to ≈ 4 GB mem / 8 GB disk. |
| Regressing the working Python corpus | Parallel track: separate dir, separate envs, separate module; core tweaks limited to cache-ignore globs which are safe for both. |

---

## 9. Acceptance criteria for SP1

1. **`validate`** on the slice confirms the admission gate: the initial (unsolved)
   `repo/` fails ≥1 check, and the reference-patched repo passes all checks.
2. **`finalize`** mechanically generates `reference.patch` from the unsolved repo →
   the hand-authored fixed repo (never hand-written).
3. A **10-rollout `measure`** runs end-to-end through the new
   `evolving-coding-agent-webapp-solver-opencode` env and produces a real
   pass-rate number recorded into `task.toml`.
4. The loop is **reproducible**: two independent runs of the check harness on the
   same repo state produce the same pass/fail per assertion.
5. The existing Python corpus, envs, tests, and local gate are **unaffected**
   (existing `pytest tests/` still passes).

---

## 10. Open questions (low-stakes, resolvable in implementation)

- Exact Node LTS version to pin (e.g. 20.x vs 22.x) — pick the latest LTS that
  installs cleanly in `python:3.11-slim`.
- Exact student model for the webapp gate — likely larger than `Qwen/Qwen3.5-4B`
  given React generation; finalized when SP4 calibrates difficulty. SP1 only needs
  *a* number, so any configured student is fine.
- Whether to cache `npm ci` between `correctness` and `anticheat` within one
  rollout (optimization, not correctness).

None of these block implementation of SP1.
