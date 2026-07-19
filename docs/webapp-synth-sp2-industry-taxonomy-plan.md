# SP2 — Industry Taxonomy & Seed Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Author the webapp taxonomy (industries × archetypes × component-anchored seeds) as a markdown library with a parser + checkability gate, and prove it yields gradeable tasks by building 2–3 validation tasks end-to-end through the SP1 substrate.

**Architecture:** A `webapp_synth/taxonomy/` subpackage holds a human-authored `webapp_library.md` and a `seeds.py` parser (mirrors evolve-cc's `domain-library.md` + `extract_seeds.py`). Seeds anchor on component/interaction rules (difficulty + checkability); industry × archetype are orthogonal theming axes. Validation tasks reuse the entire SP1 substrate (React/Vite/Tailwind repo + vitest/jsdom checks + `finalize`/`validate`), adding only industry-specific components + per-seed assertions.

**Tech Stack:** Python 3.10+ (`pytest`), React 18 + Vite + TypeScript + Tailwind, Vitest + React Testing Library + jsdom, the `evolving-coding-agent` CLI.

**Spec:** `docs/webapp-synth-sp2-industry-taxonomy-design.md`

**Conventions:**
- Work in `/Users/sidgraph/webapp-synth` on branch `main`. Node is on the host.
- Append the trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` to every commit.
- Run Python via `uv run`; use `uv run --with pytest --with pytest-asyncio pytest ...` where pytest isn't in the base env.
- **`anticheat.py` is TASK-SPECIFIC, not copyable from SP1.** SP1's `anticheat.py` hardcodes
  SP1 component filenames (`Nav.tsx`/`MobileMenu.tsx`/`Sections.tsx`) + the `mobile-menu`
  string, so copying it into a new task makes the reference repo fail anticheat and
  `validate` FAIL. Each task's `anticheat.py` must list ITS OWN required component files +
  a component-specific marker string before running `anticheat.test.tsx`. Tasks 3–5 give the
  exact per-task `anticheat.py` to write. (`correctness.py` and `_vitest.py` ARE generic —
  copy them unchanged.)

---

## File Structure

**New**
- `webapp_synth/taxonomy/__init__.py` — subpackage marker.
- `webapp_synth/taxonomy/webapp_library.md` — the taxonomy: `## industries`, `## archetypes`, `## seeds` (component tables), `## difficulty_principles`.
- `webapp_synth/taxonomy/seeds.py` — parser (`Seed`, `WorkItem`, `parse_seeds`, `industries`, `archetypes`, `work_items`, `validate_checkable`).
- `tests/test_taxonomy.py` — parser + checkability tests.
- `tasks_web/dental_clinic_form_validation_t0/` — validation task 1 (lead_gen, `form_validation_gating`).
- `tasks_web/restaurant_accordion_single_t0/` — validation task 2 (landing, `accordion_single_open`).
- `tasks_web/fitness_responsive_grid_t0/` — validation task 3 (landing, `responsive_grid_collapse`) — **optional**.

**Reused (copied per validation task, unchanged from SP1's `taskflow_repair_t0`):** the Vite/Tailwind/TS config files, `checks/_vitest.py`, `checks/correctness.py`, `checks/anticheat.py`, `checks/web/vitest.config.ts`, `checks/web/setup.ts`.

---

## Task 1: The taxonomy library (content)

**Files:**
- Create: `webapp_synth/taxonomy/__init__.py`
- Create: `webapp_synth/taxonomy/webapp_library.md`

- [ ] **Step 1: Create the subpackage marker**

Create `webapp_synth/taxonomy/__init__.py`:
```python
"""Webapp taxonomy: industries, archetypes, and component-anchored seeds."""
```

- [ ] **Step 2: Author the taxonomy library**

Create `webapp_synth/taxonomy/webapp_library.md`:
````markdown
# Webapp taxonomy & seed library

Seeds anchor on a component/interaction RULE (which supplies difficulty + deterministic
checkability). Industry × archetype are orthogonal theming axes any seed drops into.
Every seed row MUST have an `assertion_hint` (how it is checked in vitest/jsdom).

## industries
| id | description |
| saas | B2B software product marketing site |
| dental_clinic | local dental practice |
| restaurant | independent restaurant / cafe |
| fitness_studio | boutique gym / fitness studio |

## archetypes
| id | description |
| landing | hero + marketing sections (features/pricing/FAQ/footer) |
| lead_gen | contact/booking page centered on a form |

## seeds

### nav
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| mobile_menu_close_on_navigate | tapping a menu link closes the mobile menu | on phone the menu stays open covering the page after choosing a destination | open menu (click nav-toggle), click a link in mobile-menu, assert queryByTestId mobile-menu is null | t0 | scroll_spy_active_link |
| scroll_spy_active_link | the in-view section's nav link is marked active | the nav never highlights where you are on the page | mock IntersectionObserver in setup; drive a section into view; assert its link has the active class or aria-current true | t2-t3 | mobile_menu_close_on_navigate |

### accordion
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| accordion_single_open | opening one FAQ item closes the others | multiple FAQ answers stay expanded at once | open item A then item B, assert exactly one faq-answer in the document | t0 | a11y_labels_alt |

### grid
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| responsive_grid_collapse | the card grid is one column on mobile, multi on desktop | cards stay in a cramped multi-column row on phones | assert the grid element className contains grid-cols-1 and a md:grid-cols- class | t0 | filter_list |

### a11y
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| a11y_labels_alt | images have alt text, icon-buttons have aria-label, inputs have labels | screen readers cannot announce images or controls | assert every img has non-empty alt, icon buttons expose an accessible name, getByLabelText finds each input | t0-t1 | form_validation_gating |

### pricing
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| pricing_most_popular | exactly the intended tier carries the most-popular highlight | the highlight is missing or on the wrong plan | assert exactly one popular-badge and it is within the intended tier matched by name or order | t1 | tabs_active_panel |

### form
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| form_validation_gating | submitting invalid input is blocked and shows errors | the contact form submits even when required fields are empty or bad | submit empty then assert error messages shown and no success state, fill valid then assert success state | t1 | controlled_input_state |
| controlled_input_state | inputs are controlled and reflect typed text | typing in a field does nothing or the value never updates | user-event type into the input, assert input value equals the typed text | t2 | form_validation_gating |

### tabs
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| tabs_active_panel | selecting a tab shows only its panel | wrong panel shows or multiple panels show at once | click tab 2, assert exactly one tabpanel visible and it is panel 2 with aria-selected true | t1 | pricing_most_popular |

### modal
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| modal_close_overlay_esc | the modal closes on overlay click and on Escape | the popup will not dismiss without the X button | open modal, click overlay assert gone, reopen, press Escape assert gone | t1-t2 | controlled_input_state |

### carousel
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| carousel_wrap_bounds | next and prev wrap within bounds, never off the ends | the testimonial slider goes blank past the last slide | click next past the end, assert the active slide index wraps or stays within range | t2 | filter_list |

### filter
| seed_id | rule | symptom_surface | assertion_hint | difficulty | couples_with |
| filter_list | category buttons filter the list and All restores it | filtering does nothing or All hides everything | click a category assert only matching items render, click All assert full set renders | t2 | responsive_grid_collapse |

## difficulty_principles

- Reason-it-out, not recalled-reflex: a t2+ defect must be a repo-specific rule the
  student reads and reasons about, not a canonical fix it recalls. t0/t1 seeds may be
  single-component reflexes (a missing onClick, a missing responsive class).
- Difficulty = reasoning depth, not page size. More sections or copy is not harder.
- Coupling is a multiplier on already-unfamiliar defects, via couples_with: cross-component
  state (scroll_spy + mobile_menu_close), form state (form_validation + controlled_input),
  layout+behavior (filter_list + responsive_grid_collapse). Coupling easy reflexes does not
  create difficulty.
- Tier intent: t0 = one single-component reflex; t1 = one non-obvious single-component rule;
  t2+ = coupled / cross-component reasoning or state/observer subtleties. Bands are measured
  in SP4.
- Determinism: every seed's assertion_hint must be a deterministic vitest/jsdom assertion.
  Observer/timer seeds (scroll_spy_active_link) must mock the boundary (IntersectionObserver)
  in setup.ts.
````

- [ ] **Step 3: Commit**

```bash
git add webapp_synth/taxonomy/__init__.py webapp_synth/taxonomy/webapp_library.md
git commit -m "feat(taxonomy): webapp seed library (industries, archetypes, 12 seeds)"
```

---

## Task 2: The parser + checkability gate (TDD)

**Files:**
- Create: `tests/test_taxonomy.py`
- Create: `webapp_synth/taxonomy/seeds.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_taxonomy.py`:
```python
from webapp_synth.taxonomy import seeds as T


def test_library_parses_expected_shape():
    s = T.parse_seeds()
    ids = {x.seed_id for x in s}
    assert "mobile_menu_close_on_navigate" in ids
    assert "form_validation_gating" in ids
    assert len(s) >= 12
    components = {x.component for x in s}
    assert {"nav", "accordion", "form", "grid"} <= components


def test_industries_and_archetypes():
    assert set(T.industries()) >= {"saas", "dental_clinic", "restaurant", "fitness_studio"}
    assert set(T.archetypes()) >= {"landing", "lead_gen"}


def test_every_seed_is_checkable():
    assert T.validate_checkable(T.parse_seeds()) == []


def test_couples_with_all_resolve():
    s = T.parse_seeds()
    ids = {x.seed_id for x in s}
    for seed in s:
        for c in seed.couples_with:
            assert c in ids, f"{seed.seed_id} couples_with unknown seed {c}"


def test_work_items_product():
    s = T.parse_seeds()
    items = T.work_items(s, ["dental_clinic"], ["lead_gen"])
    assert len(items) == len(s)
    assert all(w.industry == "dental_clinic" and w.archetype == "lead_gen" for w in items)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run --with pytest pytest tests/test_taxonomy.py -v`
Expected: FAIL — `webapp_synth.taxonomy.seeds` does not exist.

- [ ] **Step 3: Implement the parser**

Create `webapp_synth/taxonomy/seeds.py`:
```python
"""Parser for webapp_library.md (industries, archetypes, component-anchored seeds).

Mirrors evolve-cc's extract_seeds.py: reads markdown tables into structured records.
The assertion_hint column is the checkability contract — validate_checkable() rejects
any seed without one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from itertools import product
from pathlib import Path

DEFAULT_LIBRARY = Path(__file__).with_name("webapp_library.md")


@dataclass(frozen=True)
class Seed:
    seed_id: str
    component: str
    rule: str
    symptom: str
    assertion_hint: str
    difficulty: str
    couples_with: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkItem:
    seed: Seed
    industry: str
    archetype: str


def _read(md_path: Path | str) -> str:
    return Path(md_path).read_text()


def _section(md: str, heading: str) -> str:
    """Body of a `## <heading>` section, up to the next `## ` (not `### `) or EOF."""
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", re.M | re.S)
    m = pat.search(md)
    return m.group(1) if m else ""


def _is_separator(cells: list[str]) -> bool:
    return set("".join(cells)) <= set("-: ")


def _id_column(md: str, heading: str) -> list[str]:
    out: list[str] = []
    for line in _section(md, heading).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        first = cells[0].strip("` ")
        if first.lower() == "id" or _is_separator(cells):
            continue
        out.append(first)
    return out


def industries(md_path: Path | str = DEFAULT_LIBRARY) -> list[str]:
    return _id_column(_read(md_path), "industries")


def archetypes(md_path: Path | str = DEFAULT_LIBRARY) -> list[str]:
    return _id_column(_read(md_path), "archetypes")


def parse_seeds(md_path: Path | str = DEFAULT_LIBRARY) -> list[Seed]:
    md = _read(md_path)
    block = _section(md, "seeds")
    seeds: list[Seed] = []
    component: str | None = None
    for line in block.splitlines():
        h = re.match(r"^###\s+(.+?)\s*$", line)
        if h:
            component = h.group(1).strip()
            continue
        s = line.strip()
        if component is None or not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 6:
            continue
        seed_id = cells[0].strip("` ")
        if seed_id.lower() == "seed_id" or _is_separator(cells):
            continue
        couples = tuple(
            c.strip("` ")
            for c in cells[5].split(",")
            if c.strip() and c.strip() != "-"
        )
        seeds.append(
            Seed(
                seed_id=seed_id,
                component=component,
                rule=cells[1],
                symptom=cells[2],
                assertion_hint=cells[3],
                difficulty=cells[4],
                couples_with=couples,
            )
        )
    return seeds


def validate_checkable(seeds: list[Seed]) -> list[str]:
    """Return seed_ids missing an assertion_hint (the checkability gate). [] = ok."""
    return [s.seed_id for s in seeds if not s.assertion_hint.strip()]


def work_items(
    seeds: list[Seed],
    industries: list[str],
    archetypes: list[str],
    pairs: list[tuple[str, str]] | None = None,
) -> list[WorkItem]:
    combos = pairs if pairs is not None else list(product(industries, archetypes))
    return [
        WorkItem(seed=s, industry=i, archetype=a)
        for s in seeds
        for (i, a) in combos
    ]
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run --with pytest pytest tests/test_taxonomy.py -v`
Expected: PASS (5 tests). If `test_every_seed_is_checkable` or `test_couples_with_all_resolve` fails, the **library** (Task 1) has a gap — fix the markdown, not the test.

- [ ] **Step 5: Commit**

```bash
git add webapp_synth/taxonomy/seeds.py tests/test_taxonomy.py
git commit -m "feat(taxonomy): seed parser + checkability gate"
```

---

## Task 3: Validation task — dental_clinic_form_validation_t0

**Files:**
- Create: `tasks_web/dental_clinic_form_validation_t0/**`
- Scratch fixed repo: `/tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0/`

The defect (`form_validation_gating`): the contact form shows a success message even when required fields are empty/invalid; it should block and show errors until the input is valid.

- [ ] **Step 1: Copy the SP1 scaffold + shared checks**

Run:
```bash
cd /Users/sidgraph/webapp-synth
SRC=tasks_web/taskflow_repair_t0
DST=tasks_web/dental_clinic_form_validation_t0
mkdir -p "$DST"
cp -R "$SRC/repo" "$DST/repo"
rm -rf "$DST/repo/node_modules" "$DST/repo/dist" "$DST/repo/.eca_checks"
rm -rf "$DST/repo/src/components"
mkdir -p "$DST/checks/web"
cp "$SRC/checks/_vitest.py" "$SRC/checks/correctness.py" "$SRC/checks/anticheat.py" "$DST/checks/"
cp "$SRC/checks/web/vitest.config.ts" "$SRC/checks/web/setup.ts" "$DST/checks/web/"
```
This reuses the identical Vite/Tailwind/TS config, the Python check wrappers, and the vitest config/setup. Only the components + the two `.test.tsx` specs + `instruction.md` + `task.toml` are task-specific.

- [ ] **Step 2: Write the page (`App.tsx` + `ContactForm.tsx`) — the broken version**

Create `tasks_web/dental_clinic_form_validation_t0/repo/src/App.tsx`:
```tsx
import { ContactForm } from './components/ContactForm'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <header className="border-b">
        <div className="mx-auto max-w-3xl px-4 py-4">
          <span className="text-lg font-bold">Brightsmile Dental</span>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-16">
        <h1 className="text-3xl font-bold">Book your appointment</h1>
        <p className="mt-2 text-slate-600">
          Send us your details and our front desk will confirm your visit.
        </p>
        <ContactForm />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-3xl px-4 py-8 text-sm text-slate-500">
          © 2026 Brightsmile Dental. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
```

Create `tasks_web/dental_clinic_form_validation_t0/repo/src/components/ContactForm.tsx` (BROKEN — no validation gating):
```tsx
import { useState } from 'react'

type Errors = { name?: string; email?: string; message?: string }

export function ContactForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [errors] = useState<Errors>({})
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // BROKEN: confirms the booking without checking the inputs.
    setSubmitted(true)
  }

  return (
    <form data-testid="contact-form" onSubmit={handleSubmit} className="mt-8 space-y-4" noValidate>
      <div>
        <label htmlFor="name" className="block text-sm font-medium">Name</label>
        <input id="name" value={name} onChange={(e) => setName(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.name && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.name}</p>}
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input id="email" value={email} onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.email && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.email}</p>}
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium">Message</label>
        <textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.message && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.message}</p>}
      </div>
      <button type="submit" className="rounded-lg bg-teal-600 px-5 py-2 font-medium text-white">
        Request appointment
      </button>
      {submitted && <p data-testid="form-success" className="text-green-700">Thanks — we’ll confirm shortly.</p>}
    </form>
  )
}
```

- [ ] **Step 3: Install + build to confirm the scaffold compiles**

Run:
```bash
cd /Users/sidgraph/webapp-synth/tasks_web/dental_clinic_form_validation_t0/repo
npm install
npm run build
cd /Users/sidgraph/webapp-synth
```
Expected: `package-lock.json` generated, `npm run build` succeeds.

- [ ] **Step 4: Write the two check specs**

Create `tasks_web/dental_clinic_form_validation_t0/checks/web/correctness.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

describe('dental contact page — structure', () => {
  it('renders the clinic name', () => {
    render(<App />)
    expect(screen.getByText(/brightsmile dental/i)).toBeInTheDocument()
  })
  it('renders a contact form', () => {
    render(<App />)
    expect(screen.getByTestId('contact-form')).toBeInTheDocument()
  })
  it('has labeled name, email, and message fields', () => {
    render(<App />)
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument()
  })
  it('has a submit button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /request appointment/i })).toBeInTheDocument()
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
})

describe('dental contact page — validation gating (the defect)', () => {
  it('shows errors when submitting an empty form', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getAllByTestId('form-error').length).toBeGreaterThan(0)
  })
  it('does NOT show success when submitting an empty form', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.queryByTestId('form-success')).toBeNull()
  })
  it('rejects an invalid email', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/email/i), 'not-an-email')
    await user.type(screen.getByLabelText(/message/i), 'Cleaning please')
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getAllByTestId('form-error').length).toBeGreaterThan(0)
    expect(screen.queryByTestId('form-success')).toBeNull()
  })
  it('accepts a fully valid submission', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByLabelText(/name/i), 'Ada')
    await user.type(screen.getByLabelText(/email/i), 'ada@example.com')
    await user.type(screen.getByLabelText(/message/i), 'Cleaning please')
    await user.click(screen.getByRole('button', { name: /request appointment/i }))
    expect(screen.getByTestId('form-success')).toBeInTheDocument()
  })
})
```

Create `tasks_web/dental_clinic_form_validation_t0/checks/web/anticheat.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

// Block deleting the form / fields to trivially pass "no success shown".
describe('anti-cheat', () => {
  it('keeps the contact form and its three labeled fields', () => {
    render(<App />)
    expect(screen.getByTestId('contact-form')).toBeInTheDocument()
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument()
  })
  it('keeps the submit button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /request appointment/i })).toBeInTheDocument()
  })
})
```

- [ ] **Step 5: Confirm RED on the broken repo**

Run:
```bash
cd /Users/sidgraph/webapp-synth/tasks_web/dental_clinic_form_validation_t0/repo
rm -rf .eca_checks && cp -R ../checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
npx vitest run .eca_checks/anticheat.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness **FAILS** (the 3 gating tests fail: empty→errors, empty→no-success, invalid-email; the "valid submission" test passes because the broken form always shows success) → 6/9; anticheat **PASSES** 2/2. If the broken repo does not fail exactly those gating tests, STOP and report the actual numbers.

- [ ] **Step 6: Build the fixed reference repo (GREEN)**

Run:
```bash
rm -rf /tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0
mkdir -p /tmp/cc-synth/fixed_repos
cp -R /Users/sidgraph/webapp-synth/tasks_web/dental_clinic_form_validation_t0/repo \
      /tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0
rm -rf /tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0/{node_modules,dist,.eca_checks}
```
Replace `/tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0/src/components/ContactForm.tsx` with the FIXED version (validates before confirming):
```tsx
import { useState } from 'react'

type Errors = { name?: string; email?: string; message?: string }

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function ContactForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [errors, setErrors] = useState<Errors>({})
  const [submitted, setSubmitted] = useState(false)

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const next: Errors = {}
    if (!name.trim()) next.name = 'Please enter your name.'
    if (!EMAIL_RE.test(email)) next.email = 'Please enter a valid email.'
    if (!message.trim()) next.message = 'Please enter a message.'
    setErrors(next)
    if (Object.keys(next).length > 0) {
      setSubmitted(false)
      return
    }
    setSubmitted(true)
  }

  return (
    <form data-testid="contact-form" onSubmit={handleSubmit} className="mt-8 space-y-4" noValidate>
      <div>
        <label htmlFor="name" className="block text-sm font-medium">Name</label>
        <input id="name" value={name} onChange={(e) => setName(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.name && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.name}</p>}
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input id="email" value={email} onChange={(e) => setEmail(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.email && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.email}</p>}
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium">Message</label>
        <textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)}
          className="mt-1 w-full rounded border px-3 py-2" />
        {errors.message && <p data-testid="form-error" className="mt-1 text-sm text-red-600">{errors.message}</p>}
      </div>
      <button type="submit" className="rounded-lg bg-teal-600 px-5 py-2 font-medium text-white">
        Request appointment
      </button>
      {submitted && <p data-testid="form-success" className="text-green-700">Thanks — we’ll confirm shortly.</p>}
    </form>
  )
}
```
Then verify GREEN:
```bash
cd /tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0
npm ci
rm -rf .eca_checks && cp -R /Users/sidgraph/webapp-synth/tasks_web/dental_clinic_form_validation_t0/checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
npx vitest run .eca_checks/anticheat.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness 9/9, anticheat 2/2.

- [ ] **Step 7: Write `instruction.md` (symptom-only) and `task.toml`**

Create `tasks_web/dental_clinic_form_validation_t0/instruction.md`:
```markdown
On our appointment page, visitors can send their details and get a confirmation
message. The problem: the confirmation shows up no matter what they type — someone
can leave every field blank, or put nonsense in the email box, hit the button, and
still see "we’ll confirm shortly." Our front desk then gets empty or unusable
requests.

It should only confirm once the visitor has actually given us something we can use:
a name, a real email address, and a message. When something's missing or the email
isn't valid, the page should tell them what to fix instead of confirming.
```

Create `tasks_web/dental_clinic_form_validation_t0/task.toml`:
```toml
[metadata]
name = "dental_clinic_form_validation_t0"
description = "A dental clinic contact form confirms bookings without validating input; it should gate on required, valid fields and show errors otherwise."
tier = 0
parent = ""
domain = "dental_clinic_form_validation"
archetype = "repair"
kind = "frontend"
seed = "form_validation_gating"
industry = "dental_clinic"
page_archetype = "lead_gen"
repo_path = "repo"
reference_patch = "reference.patch"
evolution_strategies = []

[[metadata.pass_rates]]
solver = "webapp-opencode"
model = "Qwen/Qwen3.5-4B"
k = 10
value = 0.0
measured = false
in_band = false
attempts = 0

[checks]
correctness = "checks/correctness.py"
anticheat = "checks/anticheat.py"
```
(Note: `archetype = "repair"` is the evolve-cc *build* archetype; the taxonomy's page archetype is the new `page_archetype` field to avoid the name clash.)

- [ ] **Step 8: finalize + validate (the admission gate)**

Run:
```bash
cd /Users/sidgraph/webapp-synth
uv run evolving-coding-agent finalize dental_clinic_form_validation_t0 \
  --tasks-dir tasks_web \
  --fixed-repo /tmp/cc-synth/fixed_repos/dental_clinic_form_validation_t0
uv run evolving-coding-agent validate dental_clinic_form_validation_t0 --tasks-dir tasks_web
```
Expected: `finalize` writes `reference.patch` for 1 file (`ContactForm.tsx`); `validate` prints `[OK]` (initial fails ≥1 check, reference passes both). `finalize`/`validate` run `npm ci` in temp copies (1–3 min each) — let them finish.

- [ ] **Step 9: Commit**

```bash
git add tasks_web/dental_clinic_form_validation_t0
git status --short   # confirm no node_modules/ or dist/
git commit -m "feat(tasks_web): dental_clinic_form_validation_t0 (form_validation_gating seed)"
```

---

## Task 4: Validation task — restaurant_accordion_single_t0

**Files:**
- Create: `tasks_web/restaurant_accordion_single_t0/**`
- Scratch fixed repo: `/tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0/`

The defect (`accordion_single_open`): the FAQ accordion lets multiple answers stay open at once; opening one should close the others.

- [ ] **Step 1: Copy the SP1 scaffold + shared checks**

Run:
```bash
cd /Users/sidgraph/webapp-synth
SRC=tasks_web/taskflow_repair_t0
DST=tasks_web/restaurant_accordion_single_t0
mkdir -p "$DST"
cp -R "$SRC/repo" "$DST/repo"
rm -rf "$DST/repo/node_modules" "$DST/repo/dist" "$DST/repo/.eca_checks" "$DST/repo/src/components"
mkdir -p "$DST/checks/web"
cp "$SRC/checks/_vitest.py" "$SRC/checks/correctness.py" "$SRC/checks/anticheat.py" "$DST/checks/"
cp "$SRC/checks/web/vitest.config.ts" "$SRC/checks/web/setup.ts" "$DST/checks/web/"
```

- [ ] **Step 2: Write the page — the broken version**

Create `tasks_web/restaurant_accordion_single_t0/repo/src/App.tsx`:
```tsx
import { FAQ } from './components/FAQ'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <main>
        <section id="hero" className="mx-auto max-w-3xl px-4 py-16 text-center">
          <h1 className="text-4xl font-bold">Olive & Thyme</h1>
          <p className="mt-2 text-slate-600">Seasonal Mediterranean plates in the heart of town.</p>
        </section>
        <FAQ />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-3xl px-4 py-8 text-sm text-slate-500">
          © 2026 Olive &amp; Thyme.
        </div>
      </footer>
    </div>
  )
}
```

Create `tasks_web/restaurant_accordion_single_t0/repo/src/components/FAQ.tsx` (BROKEN — multiple can stay open):
```tsx
import { useState } from 'react'

const QA = [
  { q: 'Do you take reservations?', a: 'Yes, for parties of two or more, online or by phone.' },
  { q: 'Are there vegan options?', a: 'Several — the menu marks every vegan and gluten-free dish.' },
  { q: 'Is there parking?', a: 'Street parking, plus a lot behind the building after 6pm.' },
]

export function FAQ() {
  // BROKEN: each opened item is added to a set, so multiple stay open at once.
  const [open, setOpen] = useState<Set<number>>(new Set())

  function toggle(i: number) {
    setOpen((prev) => {
      const next = new Set(prev)
      next.has(i) ? next.delete(i) : next.add(i)
      return next
    })
  }

  return (
    <section id="faq" className="mx-auto max-w-2xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Good to know</h2>
      <ul className="mt-8 divide-y">
        {QA.map((item, i) => (
          <li key={item.q} className="py-3">
            <button
              type="button"
              data-testid="faq-question"
              aria-expanded={open.has(i)}
              onClick={() => toggle(i)}
              className="flex w-full justify-between text-left font-medium"
            >
              {item.q}
            </button>
            {open.has(i) && <p data-testid="faq-answer" className="mt-2 text-slate-600">{item.a}</p>}
          </li>
        ))}
      </ul>
    </section>
  )
}
```

- [ ] **Step 3: Install + build**

Run:
```bash
cd /Users/sidgraph/webapp-synth/tasks_web/restaurant_accordion_single_t0/repo
npm install && npm run build
cd /Users/sidgraph/webapp-synth
```
Expected: lockfile generated, build succeeds.

- [ ] **Step 4: Write the check specs**

Create `tasks_web/restaurant_accordion_single_t0/checks/web/correctness.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '@app/App'

describe('restaurant page — structure', () => {
  it('renders the restaurant name', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1, name: /olive & thyme/i })).toBeInTheDocument()
  })
  it('renders an FAQ with at least three questions', () => {
    render(<App />)
    expect(screen.getAllByTestId('faq-question').length).toBeGreaterThanOrEqual(3)
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
  it('opening a question reveals its answer', async () => {
    const user = userEvent.setup()
    render(<App />)
    expect(screen.queryByTestId('faq-answer')).toBeNull()
    await user.click(screen.getAllByTestId('faq-question')[0])
    expect(screen.getByTestId('faq-answer')).toBeInTheDocument()
  })
})

describe('restaurant FAQ — single-open (the defect)', () => {
  it('keeps only one answer open when a second question is clicked', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    await user.click(qs[1])
    expect(screen.getAllByTestId('faq-answer')).toHaveLength(1)
  })
  it('opening a third question still leaves exactly one open', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    await user.click(qs[1])
    await user.click(qs[2])
    expect(screen.getAllByTestId('faq-answer')).toHaveLength(1)
  })
  it('opening a second question closes the first', async () => {
    const user = userEvent.setup()
    render(<App />)
    const qs = screen.getAllByTestId('faq-question')
    await user.click(qs[0])
    const firstAnswer = screen.getByTestId('faq-answer').textContent
    await user.click(qs[1])
    const openAnswer = screen.getByTestId('faq-answer').textContent
    expect(openAnswer).not.toEqual(firstAnswer)
  })
})
```

Create `tasks_web/restaurant_accordion_single_t0/checks/web/anticheat.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

// Block deleting the FAQ so "one open at a time" passes vacuously.
describe('anti-cheat', () => {
  it('keeps an FAQ with at least three question buttons', () => {
    render(<App />)
    expect(screen.getAllByTestId('faq-question').length).toBeGreaterThanOrEqual(3)
  })
})
```

- [ ] **Step 5: Confirm RED on the broken repo**

Run:
```bash
cd /Users/sidgraph/webapp-synth/tasks_web/restaurant_accordion_single_t0/repo
rm -rf .eca_checks && cp -R ../checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
npx vitest run .eca_checks/anticheat.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness **FAILS** the three single-open tests (broken keeps multiple answers open) → 4/7; anticheat **PASSES** 1/1. If not, STOP and report actual numbers.

- [ ] **Step 6: Build the fixed reference repo (GREEN)**

Run:
```bash
rm -rf /tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0
cp -R /Users/sidgraph/webapp-synth/tasks_web/restaurant_accordion_single_t0/repo \
      /tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0
rm -rf /tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0/{node_modules,dist,.eca_checks}
```
Replace `/tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0/src/components/FAQ.tsx` with the FIXED version (single open index):
```tsx
import { useState } from 'react'

const QA = [
  { q: 'Do you take reservations?', a: 'Yes, for parties of two or more, online or by phone.' },
  { q: 'Are there vegan options?', a: 'Several — the menu marks every vegan and gluten-free dish.' },
  { q: 'Is there parking?', a: 'Street parking, plus a lot behind the building after 6pm.' },
]

export function FAQ() {
  // Single-open: opening one item closes any other.
  const [open, setOpen] = useState<number | null>(null)

  return (
    <section id="faq" className="mx-auto max-w-2xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Good to know</h2>
      <ul className="mt-8 divide-y">
        {QA.map((item, i) => (
          <li key={item.q} className="py-3">
            <button
              type="button"
              data-testid="faq-question"
              aria-expanded={open === i}
              onClick={() => setOpen(open === i ? null : i)}
              className="flex w-full justify-between text-left font-medium"
            >
              {item.q}
            </button>
            {open === i && <p data-testid="faq-answer" className="mt-2 text-slate-600">{item.a}</p>}
          </li>
        ))}
      </ul>
    </section>
  )
}
```
Verify GREEN:
```bash
cd /tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0
npm ci
rm -rf .eca_checks && cp -R /Users/sidgraph/webapp-synth/tasks_web/restaurant_accordion_single_t0/checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
npx vitest run .eca_checks/anticheat.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness 7/7, anticheat 1/1.

- [ ] **Step 7: Write `instruction.md` + `task.toml`**

Create `tasks_web/restaurant_accordion_single_t0/instruction.md`:
```markdown
The "Good to know" section on our site is a list of common questions — you tap one
and its answer slides open. It works, but it feels cluttered: tap a few questions
and every answer you opened stays open, so the page turns into a wall of text and
people lose their place.

We want it to behave like the tidy version people expect: opening a question shows
its answer and quietly closes whichever one was open before, so only one answer is
visible at a time. Tapping an open question should still collapse it.
```

Create `tasks_web/restaurant_accordion_single_t0/task.toml`:
```toml
[metadata]
name = "restaurant_accordion_single_t0"
description = "A restaurant FAQ accordion lets multiple answers stay open at once; opening one should close the others (single-open)."
tier = 0
parent = ""
domain = "restaurant_accordion_single"
archetype = "repair"
kind = "frontend"
seed = "accordion_single_open"
industry = "restaurant"
page_archetype = "landing"
repo_path = "repo"
reference_patch = "reference.patch"
evolution_strategies = []

[[metadata.pass_rates]]
solver = "webapp-opencode"
model = "Qwen/Qwen3.5-4B"
k = 10
value = 0.0
measured = false
in_band = false
attempts = 0

[checks]
correctness = "checks/correctness.py"
anticheat = "checks/anticheat.py"
```

- [ ] **Step 8: finalize + validate**

Run:
```bash
cd /Users/sidgraph/webapp-synth
uv run evolving-coding-agent finalize restaurant_accordion_single_t0 \
  --tasks-dir tasks_web \
  --fixed-repo /tmp/cc-synth/fixed_repos/restaurant_accordion_single_t0
uv run evolving-coding-agent validate restaurant_accordion_single_t0 --tasks-dir tasks_web
```
Expected: `finalize` writes `reference.patch` for 1 file (`FAQ.tsx`); `validate` prints `[OK]`.

- [ ] **Step 9: Commit**

```bash
git add tasks_web/restaurant_accordion_single_t0
git status --short
git commit -m "feat(tasks_web): restaurant_accordion_single_t0 (accordion_single_open seed)"
```

---

## Task 5 (OPTIONAL): Validation task — fitness_responsive_grid_t0

Only do this if you want a third validation task (a responsive-class assertion, distinct from behavior/form). Same shape as Task 4.

**Files:**
- Create: `tasks_web/fitness_responsive_grid_t0/**`
- Scratch fixed repo: `/tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0/`

The defect (`responsive_grid_collapse`): the class grid is fixed at 3 columns, so it doesn't collapse to one column on phones; it should be `grid-cols-1 md:grid-cols-3`.

- [ ] **Step 1: Copy the scaffold + shared checks**

Run:
```bash
cd /Users/sidgraph/webapp-synth
SRC=tasks_web/taskflow_repair_t0
DST=tasks_web/fitness_responsive_grid_t0
mkdir -p "$DST"
cp -R "$SRC/repo" "$DST/repo"
rm -rf "$DST/repo/node_modules" "$DST/repo/dist" "$DST/repo/.eca_checks" "$DST/repo/src/components"
mkdir -p "$DST/checks/web"
cp "$SRC/checks/_vitest.py" "$SRC/checks/correctness.py" "$SRC/checks/anticheat.py" "$DST/checks/"
cp "$SRC/checks/web/vitest.config.ts" "$SRC/checks/web/setup.ts" "$DST/checks/web/"
```

- [ ] **Step 2: Write the page — broken version**

Create `tasks_web/fitness_responsive_grid_t0/repo/src/App.tsx`:
```tsx
import { Classes } from './components/Classes'

export default function App() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      <main>
        <section id="hero" className="mx-auto max-w-5xl px-4 py-16 text-center">
          <h1 className="text-4xl font-bold">Ironleaf Studio</h1>
          <p className="mt-2 text-slate-600">Small-group strength and mobility classes.</p>
        </section>
        <Classes />
      </main>
      <footer className="border-t">
        <div className="mx-auto max-w-5xl px-4 py-8 text-sm text-slate-500">© 2026 Ironleaf Studio.</div>
      </footer>
    </div>
  )
}
```

Create `tasks_web/fitness_responsive_grid_t0/repo/src/components/Classes.tsx` (BROKEN — fixed 3-col grid):
```tsx
const CLASSES = [
  { name: 'Foundations', body: 'Barbell basics with coaching on every rep.' },
  { name: 'Mobility Flow', body: 'Joint-by-joint mobility to move without pain.' },
  { name: 'Conditioning', body: 'Short, hard intervals that build engine.' },
]

export function Classes() {
  return (
    <section id="classes" className="mx-auto max-w-5xl px-4 py-16">
      <h2 className="text-center text-3xl font-bold">Our classes</h2>
      {/* BROKEN: fixed 3 columns — does not collapse on small screens. */}
      <div data-testid="class-grid" className="mt-10 grid grid-cols-3 gap-6">
        {CLASSES.map((c) => (
          <div key={c.name} data-testid="class-card" className="rounded-xl border p-6">
            <h3 className="text-lg font-semibold">{c.name}</h3>
            <p className="mt-2 text-slate-600">{c.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
```

- [ ] **Step 3: Install + build**

Run: `cd tasks_web/fitness_responsive_grid_t0/repo && npm install && npm run build && cd /Users/sidgraph/webapp-synth`
Expected: lockfile generated, build succeeds.

- [ ] **Step 4: Write the check specs**

Create `tasks_web/fitness_responsive_grid_t0/checks/web/correctness.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

describe('fitness page — structure', () => {
  it('renders the studio name', () => {
    render(<App />)
    expect(screen.getByRole('heading', { level: 1, name: /ironleaf studio/i })).toBeInTheDocument()
  })
  it('renders three class cards', () => {
    render(<App />)
    expect(screen.getAllByTestId('class-card')).toHaveLength(3)
  })
  it('renders a footer', () => {
    render(<App />)
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
  })
})

describe('fitness class grid — responsive (the defect)', () => {
  it('the grid is a single column on mobile', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid').className).toContain('grid-cols-1')
  })
  it('the grid expands to multiple columns on desktop', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid').className).toMatch(/md:grid-cols-\d/)
  })
})
```

Create `tasks_web/fitness_responsive_grid_t0/checks/web/anticheat.test.tsx`:
```tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '@app/App'

describe('anti-cheat', () => {
  it('keeps the class grid with its cards', () => {
    render(<App />)
    expect(screen.getByTestId('class-grid')).toBeInTheDocument()
    expect(screen.getAllByTestId('class-card').length).toBeGreaterThanOrEqual(3)
  })
})
```

- [ ] **Step 5: Confirm RED**

Run:
```bash
cd /Users/sidgraph/webapp-synth/tasks_web/fitness_responsive_grid_t0/repo
rm -rf .eca_checks && cp -R ../checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
npx vitest run .eca_checks/anticheat.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness **FAILS** the two responsive tests (broken has `grid-cols-3`, no `grid-cols-1`/`md:`) → 3/5; anticheat PASSES 1/1.

- [ ] **Step 6: Build the fixed repo (GREEN)**

```bash
rm -rf /tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0
cp -R /Users/sidgraph/webapp-synth/tasks_web/fitness_responsive_grid_t0/repo \
      /tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0
rm -rf /tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0/{node_modules,dist,.eca_checks}
```
In `/tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0/src/components/Classes.tsx`, change the grid line to:
```tsx
      <div data-testid="class-grid" className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-3">
```
Verify GREEN:
```bash
cd /tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0
npm ci
rm -rf .eca_checks && cp -R /Users/sidgraph/webapp-synth/tasks_web/fitness_responsive_grid_t0/checks/web .eca_checks
npx vitest run .eca_checks/correctness.test.tsx --config .eca_checks/vitest.config.ts
rm -rf .eca_checks && cd /Users/sidgraph/webapp-synth
```
Expected: correctness 5/5.

- [ ] **Step 7: instruction.md + task.toml**

Create `tasks_web/fitness_responsive_grid_t0/instruction.md`:
```markdown
On the classes section of our site, the three class cards sit side by side. That
looks fine on a laptop, but on a phone the three columns get squeezed into a thin,
unreadable strip — the cards never stack. On a narrow screen the cards should sit
one under another, and only spread out into the row of three once there's enough
width for it.
```

Create `tasks_web/fitness_responsive_grid_t0/task.toml`:
```toml
[metadata]
name = "fitness_responsive_grid_t0"
description = "A fitness studio class grid is fixed at three columns and doesn't collapse on mobile; it should be one column on small screens and three on desktop."
tier = 0
parent = ""
domain = "fitness_responsive_grid"
archetype = "repair"
kind = "frontend"
seed = "responsive_grid_collapse"
industry = "fitness_studio"
page_archetype = "landing"
repo_path = "repo"
reference_patch = "reference.patch"
evolution_strategies = []

[[metadata.pass_rates]]
solver = "webapp-opencode"
model = "Qwen/Qwen3.5-4B"
k = 10
value = 0.0
measured = false
in_band = false
attempts = 0

[checks]
correctness = "checks/correctness.py"
anticheat = "checks/anticheat.py"
```

- [ ] **Step 8: finalize + validate + commit**

```bash
cd /Users/sidgraph/webapp-synth
uv run evolving-coding-agent finalize fitness_responsive_grid_t0 \
  --tasks-dir tasks_web --fixed-repo /tmp/cc-synth/fixed_repos/fitness_responsive_grid_t0
uv run evolving-coding-agent validate fitness_responsive_grid_t0 --tasks-dir tasks_web
git add tasks_web/fitness_responsive_grid_t0
git commit -m "feat(tasks_web): fitness_responsive_grid_t0 (responsive_grid_collapse seed)"
```
Expected: `validate` prints `[OK]`.

---

## Task 6: Final verification

**Files:** none (verification only).

- [ ] **Step 1: Taxonomy + full test suite pass**

Run: `uv run --with pytest --with pytest-asyncio pytest tests/ -q`
Expected: all tests pass (the SP1 module tests + `test_frontend_vitest_parse` + `test_taxonomy`).

- [ ] **Step 2: The taxonomy library is discoverable via the installed package**

Run:
```bash
uv run python -c "from webapp_synth.taxonomy import seeds; print(len(seeds.parse_seeds()), 'seeds;', 'checkable:', seeds.validate_checkable(seeds.parse_seeds()) == [])"
```
Expected: `12 seeds; checkable: True` (the `.md` resolves next to `seeds.py` inside the package).

- [ ] **Step 3: All validation tasks pass the admission gate**

Run: `uv run evolving-coding-agent validate --tasks-dir tasks_web 2>&1 | tail -20`
Expected: every `tasks_web/*` task (TaskFlow + the SP2 validation tasks) reports `[OK]`.

- [ ] **Step 4: Push**

```bash
git push origin main
```

---

## Self-Review

**Spec coverage:**
- §3 taxonomy structure (industries/archetypes/seed schema) → Task 1 (markdown) + Task 2 (`industries`/`archetypes`/`Seed`).
- §4 seed library (12 seeds) + difficulty principles → Task 1.
- §5 parser + checkability gate → Task 2 (`parse_seeds`, `work_items`, `validate_checkable`).
- §6 validation set (2–3 tasks via SP1 substrate) → Tasks 3, 4, 5(optional).
- §7 file layout + reuse + packaging → File Structure section + Task 6 Step 2 (package discoverability).
- §8 acceptance criteria → Task 6 (tests pass, library checkable, all tasks `[OK]`, existing suite green).

**Placeholder scan:** no TBD/TODO; every code step shows complete code; `value=0.0`/`measured=false` are the intentional pre-measurement placeholders (SP4 fills them).

**Type/name consistency:** the `Seed` fields (`seed_id`, `component`, `rule`, `symptom`, `assertion_hint`, `difficulty`, `couples_with`) match between `seeds.py`, the tests, and the 6-column markdown tables. `data-testid`s are consistent between each task's components and its specs (`contact-form`/`form-error`/`form-success`; `faq-question`/`faq-answer`; `class-grid`/`class-card`). `task.toml` uses `archetype="repair"` (build) + `page_archetype` (taxonomy) consistently across all three tasks. The `@app` alias + `.eca_checks` harness flow matches SP1's `checks/web/vitest.config.ts` (copied unchanged).

**Note on markdown parsing:** `assertion_hint` cells must contain no literal `|` (the row splits on `|`); the authored hints use words ("or"/commas) instead — verified in Task 1.
