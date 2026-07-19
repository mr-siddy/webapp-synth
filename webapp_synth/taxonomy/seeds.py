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
