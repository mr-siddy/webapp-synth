"""Unit tests for the webapp_synth solver module (orchestrator-side, no live sandbox)."""


def test_frontend_harness_installs_node():
    from webapp_synth.harness import NODE_INSTALL_SCRIPT, frontend_repo_harness

    assert "nodejs.org" in NODE_INSTALL_SCRIPT
    assert "node --version" in NODE_INSTALL_SCRIPT
    harness = frontend_repo_harness()
    # node install is appended after the base opencode + python install
    assert "nodejs.org" in (harness.install_script or "")


def test_frontend_taskset_loads_slice_with_node_sandbox():
    from webapp_synth.taskset import FrontendHarnessTaskSet, TASKS_WEB_DIR

    ts = FrontendHarnessTaskSet(tasks_dir=TASKS_WEB_DIR)
    names = {row["info"]["task_name"] for row in ts.get_dataset()}
    assert "taskflow_repair_t0" in names

    info = {"task_name": "taskflow_repair_t0"}
    spec = ts.get_sandbox_spec(info)
    assert spec.memory_gb == 4
    assert spec.disk_size_gb == 8
    assert ts.source_tasks_subdir == "tasks_web"
    assert ts.get_workdir(info).endswith("/tasks/taskflow_repair_t0/repo")


def test_frontend_rubric_is_a_coding_rubric():
    from evolving_coding_agent.taskset import CodingRubric
    from webapp_synth.rubric import FrontendRubric

    r = FrontendRubric()
    assert isinstance(r, CodingRubric)  # reuses graded_reward + metrics
    assert hasattr(r, "_score_in_sandbox_frontend")


def test_frontend_env_builds_environment():
    from webapp_synth.env import load_environment

    env = load_environment(task="taskflow_repair_t0")
    assert env is not None  # ComposableEnv constructed without spinning a sandbox


def test_webapp_shim_resolves():
    import webapp_synth_solver_opencode as shim

    assert hasattr(shim, "load_environment")
