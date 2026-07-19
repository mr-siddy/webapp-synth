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
