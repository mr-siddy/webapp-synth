import importlib.util
from pathlib import Path

CHECKS = Path("tasks_web/taskflow_repair_t0/checks")


def _load(name: str):
    path = CHECKS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_eca_test_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, str(CHECKS))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(CHECKS))
    return mod


def test_parse_vitest_json_counts_pass_total():
    v = _load("_vitest")
    sample = (
        'noise line\n'
        '{"numTotalTests": 11, "numPassedTests": 8, "numFailedTests": 3, "success": false}\n'
    )
    assert v._parse_vitest_json(sample) == (8, 11)


def test_parse_vitest_json_handles_garbage():
    v = _load("_vitest")
    assert v._parse_vitest_json("not json at all") == (0, 0)
