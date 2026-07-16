# SP2 — Industry Taxonomy & Seed Library (minimal slice)

- **Date:** 2026-07-16
- **Status:** Approved design, ready for implementation planning
- **Repo:** `webapp-synth` (depends on `evolving-coding-agent`)
- **Predecessor:** SP1 (frontend task substrate) — proven; see `docs/webapp-synth-sp1-frontend-substrate.md`.

---

## 1. Context & motivation

SP1 proved the substrate: a React/Tailwind landing-page task can be built, rendered
(vitest/jsdom), and scored deterministically through the reused
`evolving-coding-agent` engine (`score`, `finalize`, `validate`). SP2 supplies the
**menu** that later sub-projects iterate over — the webapp analog of evolve-cc's
`domain-library.md` (30 roots + 180 library rule-seeds) plus `extract_seeds.py`.

SP2 defines **what tasks exist** (industries × page archetypes × component/interaction
seeds) and the **difficulty principles** for frontend, and provides a **parser** that
turns the human-authored menu into structured work items. It feeds SP3 (the page
generator) and SP4 (task-derivation + pass-rate calibration).

### Decisions locked during brainstorming

1. **Scope:** minimal complete slice — prove the taxonomy → gradeable-task pipeline,
   don't scale content.
2. **Format:** human-authored **markdown tables + a parser** (mirrors evolve-cc's
   `domain-library.md` + `extract_seeds.py`). Most editable for humans and the synth
   agent; proven at 180-seed scale.
3. **Difficulty:** **principles + per-seed hints** in SP2; actual pass-rate band
   calibration stays in SP4 (which measures).
4. **Seed anchor:** **component/interaction-anchored** — each seed anchors on a UI
   component/interaction rule that supplies difficulty + checkability; **industry ×
   archetype are orthogonal theming axes** any seed drops into. (The SP1 mobile-menu
   bug is a component rule; "TaskFlow SaaS" was just theming.)

---

## 2. Scope

**In scope**

- The taxonomy structure: industry + archetype vocabularies, and the
  component-anchored seed library (~12 seeds) as markdown tables.
- The frontend **difficulty-principles** section + per-seed difficulty hints.
- A **parser** (`webapp_synth/taxonomy/seeds.py`) that reads the markdown into
  structured `Seed`/`WorkItem` records, with a **checkability gate**.
- Unit tests for the parser + the checkability invariant.
- **2–3 validation tasks** built end-to-end through the SP1 substrate, each a
  *different* industry/archetype/seed than TaskFlow, each passing the RED→GREEN
  `validate` gate.

**Out of scope (later)**

- The full 15–30 industry / 100+ seed library (a later content pass).
- Pass-rate band calibration and the full t0–t4 tier ladder (SP4).
- The page generator + quality judge + SFT pairs (SP3).
- Any automated `synthesize-webapp-task` skill that consumes the taxonomy — for SP2,
  the validation tasks are authored by hand using the SP1 pattern (the skill is
  SP3/SP4).

---

## 3. Taxonomy structure & seed schema

Three axes; seeds anchor on the component/interaction rule; industry × archetype are
orthogonal.

- **Industries (slice):** `saas`, `dental_clinic`, `restaurant`, `fitness_studio`.
- **Archetypes (slice):** `landing` (hero + marketing sections), `lead_gen`
  (contact/booking, form-centric).

### Markdown layout (what the parser reads)

```
## industries
| id | description |
| saas | B2B software product marketing site |
| dental_clinic | local dental practice |
| ...

## archetypes
| id | description |
| landing | hero + features/pricing/FAQ/footer marketing page |
| lead_gen | contact/booking page centered on a form |

## seeds
### <component>            (e.g. ### nav, ### accordion, ### form, ### grid, ...)
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| ...     | ...  | ...             | ...            | ...        | ...          |

## difficulty_principles
<prose — not parsed>
```

### Seed record (one table row → one `Seed`)

| field | meaning |
|---|---|
| `component` | from the `### <component>` heading |
| `seed_id` | unique snake_case id |
| `rule` | the repo-specific correct behavior the defect violates |
| `symptom_surface` | the user-visible symptom (what an `instruction.md` may describe) — never names the fix |
| `assertion_hint` | **mandatory** — how it is asserted in vitest/jsdom (the checkability contract) |
| `difficulty` | starting-tier hint, e.g. `t0`, `t1`, `t2-t3` (a hint, not a measured band) |
| `couples_with` | comma-separated `seed_id`s that combine into higher tiers |

The **`assertion_hint` is required**: a seed with no deterministic vitest/jsdom
assertion cannot enter the RL menu (aesthetic-only quality belongs to SP3's judge).

---

## 4. The seed library (the ~12 slice seeds)

Grouped by component. `assertion_hint` uses React Testing Library / `user-event`
against jsdom (the SP1 harness).

### nav
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `mobile_menu_close_on_navigate` | tapping a menu link closes the mobile menu | on phone the menu stays open covering the page after choosing a destination | open menu (click `nav-toggle`), click a link in `mobile-menu`, assert `queryByTestId('mobile-menu')` is null | t0 | `scroll_spy_active_link` |
| `scroll_spy_active_link` | the in-view section's nav link is marked active | the nav never highlights where you are on the page | mock `IntersectionObserver` in setup; drive a section into view; assert its link has the active class / `aria-current="true"` | t2-t3 | `mobile_menu_close_on_navigate` |

### accordion
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `accordion_single_open` | opening one FAQ item closes the others | multiple FAQ answers stay expanded at once | open item A then item B; assert exactly one `faq-answer` in the document | t0 | `a11y_labels_alt` |

### grid
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `responsive_grid_collapse` | the card grid is 1 column on mobile, multi on desktop | cards stay in a cramped multi-column row on phones | assert the grid element `className` contains `grid-cols-1` and a `md:grid-cols-*` | t0 | `filter_list` |

### a11y
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `a11y_labels_alt` | images have alt text, icon-buttons have `aria-label`, inputs have labels | screen readers can't announce images/controls | assert every `<img>` has non-empty `alt`; icon buttons expose an accessible name; `getByLabelText` finds each input | t0-t1 | `form_validation_gating` |

### pricing
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `pricing_most_popular` | exactly the intended tier carries the "most popular" highlight | the highlight is missing or on the wrong plan | assert exactly one `popular-badge`, and it is within the intended tier (matched by tier name/order) | t1 | `tabs_active_panel` |

### form
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `form_validation_gating` | submitting invalid input is blocked and shows errors | the contact form "submits" even when required fields are empty/bad | submit empty → assert error message(s) shown AND no success state (`success` testid absent); fill valid → assert success state | t1 | `controlled_input_state`, `a11y_labels_alt` |
| `controlled_input_state` | inputs are controlled and reflect typed text | typing in a field does nothing / value never updates | `user-event` type into the input; assert `input.value` equals the typed text | t2 | `form_validation_gating` |

### tabs
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `tabs_active_panel` | selecting a tab shows only its panel | wrong panel shows, or multiple panels show at once | click tab 2; assert exactly one `tabpanel` visible and it is panel 2; `aria-selected="true"` on tab 2 | t1 | `pricing_most_popular` |

### modal
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `modal_close_overlay_esc` | the modal closes on overlay click and on Escape | the popup won't dismiss without the X button | open modal; click overlay → assert gone; reopen; press `Escape` → assert gone | t1-t2 | `controlled_input_state` |

### carousel
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `carousel_wrap_bounds` | next/prev wrap within bounds, never off the ends | the testimonial slider goes blank past the last slide | click next past the end; assert the active slide index wraps / stays in `[0, n)` | t2 | `filter_list` |

### filter
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
|---|---|---|---|---|---|
| `filter_list` | category buttons filter the list; "All" restores it | filtering does nothing, or "All" hides everything | click a category → assert only matching items render; click "All" → assert full set renders | t2 | `responsive_grid_collapse` |

### Difficulty principles (the `## difficulty_principles` prose)

- **Reason-it-out, not recalled-reflex:** a t2+ defect must be a repo-specific rule the
  student must read and reason about, not a canonical fix it recalls (mirrors evolve-cc).
  t0/t1 seeds may be single-component reflexes (a missing `onClick`, a missing
  responsive class).
- **Difficulty = reasoning depth, not page size.** More sections/copy is not harder.
- **Coupling is a multiplier on already-unfamiliar defects**, via `couples_with`:
  cross-component state (`scroll_spy` + `mobile_menu_close`), form state
  (`form_validation` + `controlled_input`), layout+behavior (`filter_list` +
  `responsive_grid_collapse`). Coupling easy reflexes does not create difficulty.
- **Tier intent:** t0 = one single-component reflex; t1 = one non-obvious
  single-component rule; t2+ = coupled / cross-component reasoning or state/observer
  subtleties. Actual bands are measured in SP4.
- **Determinism:** every seed's `assertion_hint` must be a deterministic vitest/jsdom
  assertion. Observer/timer-based seeds (`scroll_spy_active_link`) must mock the
  boundary (`IntersectionObserver`) in `setup.ts`.

---

## 5. Parser + checkability gate

`webapp_synth/taxonomy/seeds.py`:

```python
@dataclass
class Seed:
    seed_id: str
    component: str
    rule: str
    symptom: str
    assertion_hint: str
    difficulty: str
    couples_with: list[str]

@dataclass
class WorkItem:
    seed: Seed
    industry: str
    archetype: str

DEFAULT_LIBRARY = Path(__file__).with_name("webapp_library.md")

def parse_seeds(md_path: Path = DEFAULT_LIBRARY) -> list[Seed]: ...
def industries(md_path: Path = DEFAULT_LIBRARY) -> list[str]: ...   # ids
def archetypes(md_path: Path = DEFAULT_LIBRARY) -> list[str]: ...   # ids
def work_items(seeds, industries, archetypes,
               pairs: list[tuple[str, str]] | None = None) -> list[WorkItem]: ...
def validate_checkable(seeds) -> list[str]:   # seed_ids with empty assertion_hint; [] = ok
    ...
```

- `parse_seeds` reads `## seeds` → `### <component>` tables (same shape as
  `extract_seeds.py` reads `## library_rule_seeds` → `### <lib>`), splitting
  `couples_with` on commas.
- `work_items` yields the seed × industry × archetype product (or a curated `pairs`
  subset) for orchestration to iterate.
- `validate_checkable` is the **gate**: any seed missing an `assertion_hint` is
  reported; a non-empty result is a build error.

`tests/test_taxonomy.py`: assert the library parses to the expected seed count and
components, `couples_with` references resolve to real `seed_id`s, `industries()`/
`archetypes()` return the slice vocabularies, and `validate_checkable(parse_seeds())
== []` (every seed is checkable).

---

## 6. Validation set (proves the taxonomy yields gradeable tasks)

Build these end-to-end through the **SP1 substrate** (React repo + `checks/web/` vitest
harness + `checks/*.py` wrappers + `finalize`/`validate` + `kind = "frontend"`), each a
*different* industry/archetype/seed than TaskFlow:

1. `dental_clinic_form_validation_t0` — `lead_gen` contact page; seed
   `form_validation_gating`. Broken repo submits an empty form; fix gates on validation.
2. `restaurant_accordion_single_t0` — `landing`; seed `accordion_single_open`. Broken
   repo lets multiple FAQ/menu items stay open; fix makes it single-open.
3. *(optional 3rd)* `fitness_responsive_grid_t0` — `landing`; seed
   `responsive_grid_collapse`. Broken repo's class-list omits `grid-cols-1`; fix adds it.

Each must satisfy the admission gate: initial repo fails ≥1 check, reference-patched
repo passes all, `evolving-coding-agent validate <task> --tasks-dir tasks_web` → `[OK]`.
Their `task.toml` records the seed + industry + archetype (`domain = "<industry>_<seed>"`,
plus `metadata` fields `seed`, `industry`, `archetype`).

---

## 7. File layout & reuse

**New (in `webapp-synth`):**
- `webapp_synth/taxonomy/__init__.py`
- `webapp_synth/taxonomy/webapp_library.md` — the taxonomy + seed tables + principles.
- `webapp_synth/taxonomy/seeds.py` — the parser + checkability gate.
- `tests/test_taxonomy.py`
- `tasks_web/dental_clinic_form_validation_t0/`, `tasks_web/restaurant_accordion_single_t0/`,
  and optionally `tasks_web/fitness_responsive_grid_t0/`.

**Reused verbatim:** the entire SP1 substrate — the React/Vite/Tailwind scaffold pattern,
the vitest/jsdom harness (`checks/web/`), the Python check wrappers (`checks/_vitest.py`,
`correctness.py`, `anticheat.py`), `finalize`/`validate`/`score`, and the
`webapp-synth-solver-opencode` env. SP2 adds no new scoring machinery.

**Package the library:** add `webapp_synth/taxonomy/webapp_library.md` to the wheel
(hatch `force-include` or `artifacts`) so `parse_seeds(DEFAULT_LIBRARY)` resolves when
installed.

---

## 8. Acceptance criteria

1. `webapp_synth/taxonomy/webapp_library.md` authored: `## industries`, `## archetypes`,
   the ~12 component-anchored seeds, and `## difficulty_principles`.
2. `uv run pytest tests/test_taxonomy.py` passes: correct seed count/components,
   `couples_with` all resolve, and `validate_checkable(parse_seeds()) == []`.
3. The 2 (or 3) validation tasks each pass `evolving-coding-agent validate <task>
   --tasks-dir tasks_web` → `[OK]` (RED→GREEN admission gate) via the SP1 substrate.
4. The existing test suite still passes (`uv run pytest tests/ -q`).

---

## 9. Out of scope / future

- SP4 measures pass-rates and calibrates the `difficulty` hints into real bands, and
  grows each validation task into a t0–t4 ladder via `couples_with`.
- SP3 builds the generator + quality judge that consume `work_items(...)`.
- The full industry/archetype/seed library (this slice is a representative starter).
- An automated skill/orchestration loop over `work_items` (SP3/SP4).
