"""Anti-cheat gate: required components present + the menu really renders links."""

from pathlib import Path

from _vitest import run_vitest

REQUIRED = [
    "src/App.tsx",
    "src/components/Nav.tsx",
    "src/components/MobileMenu.tsx",
    "src/components/Sections.tsx",
]


def check(repo_path, task_dir, reference_repo_path=None):
    repo = Path(repo_path)
    for rel in REQUIRED:
        if not (repo / rel).is_file():
            return {"passed": False, "message": f"required file removed: {rel}"}
    menu = (repo / "src/components/MobileMenu.tsx").read_text()
    if "mobile-menu" not in menu:
        return {"passed": False, "message": "mobile-menu element removed"}
    passed, total, tail = run_vitest(repo, task_dir, "anticheat.test.tsx")
    ok = total > 0 and passed == total
    return {
        "passed": ok,
        "message": "anticheat ok" if ok else f"anticheat {passed}/{total}: {tail}",
    }
