"""Functional check: fraction of vitest correctness assertions that pass."""

from _vitest import run_vitest


def check(repo_path, task_dir, reference_repo_path=None):
    passed, total, tail = run_vitest(repo_path, task_dir, "correctness.test.tsx")
    if total == 0:
        return {"score": 0.0, "passed": False, "message": f"no tests ran: {tail}"}
    return {
        "score": passed / total,
        "passed": passed == total,
        "message": f"{passed}/{total} correctness assertions passed",
    }
