"""Tests for the scaffold-agentic-app generator (`scaffold.py`).

Characterization tests: the generator already exists, so these pin its current
contract — produces the expected tree, the output compiles, and re-running is
idempotent (never overwrites).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAFFOLD = REPO / "skills" / "scaffold-agentic-app" / "scaffold.py"

# A representative slice of the tree, including the gap-fills (package markers,
# kept-empty data dirs, CI) that the generator adds beyond the source diagram.
EXPECTED = [
    "app/main.py",
    "app/config.py",
    "app/schemas.py",
    "app/__init__.py",
    "app/agent/orchestrator.py",
    "app/agent/tools/web_search.py",
    "app/eval/input_quality.py",
    "app/tracing/cost_tracker.py",
    "app/data/raw/.gitkeep",
    "tests/test_retrieval.py",
    "tests/test_config.py",
    "tests/test_health.py",
    ".github/workflows/ci.yml",
    ".github/dependabot.yml",
    ".dockerignore",
]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCAFFOLD), *args], capture_output=True, text=True
    )


def test_generates_expected_tree(tmp_path: Path) -> None:
    target = tmp_path / "app"
    result = _run(str(target))
    assert result.returncode == 0, result.stdout + result.stderr
    for rel in EXPECTED:
        assert (target / rel).is_file(), f"missing generated file: {rel}"


def test_generated_python_compiles(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    result = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", str(target)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_rerun_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    second = _run(str(target))
    assert second.returncode == 0
    assert "created: 0 file(s)" in second.stdout


def test_appends_to_existing_claude_md_without_clobbering(tmp_path: Path) -> None:
    target = tmp_path / "app"
    target.mkdir()
    claude = target / "CLAUDE.md"
    claude.write_text("# My project memory\nkeep me\n")

    result = _run(str(target))
    assert result.returncode == 0
    text = claude.read_text()
    assert "keep me" in text  # the project's own content is preserved
    assert "BEGIN scaffold-agentic-app" in text  # our block is appended
    assert "appended" in result.stdout


def test_append_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "app"
    target.mkdir()
    (target / "CLAUDE.md").write_text("# mine\n")

    _run(str(target))
    after_first = (target / "CLAUDE.md").read_text()
    _run(str(target))
    after_second = (target / "CLAUDE.md").read_text()

    assert after_first == after_second  # no second append
    assert after_first.count("BEGIN scaffold-agentic-app") == 1


def test_fresh_claude_md_carries_marker(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    assert "BEGIN scaffold-agentic-app" in (target / "CLAUDE.md").read_text()


def test_dockerignore_keeps_secrets_out_of_the_images(tmp_path: Path) -> None:
    # Every generated Dockerfile does `COPY . .`, and the README tells the user to create .env.
    target = tmp_path / "app"
    _run(str(target))
    dockerfiles = sorted(target.rglob("Dockerfile"))
    assert dockerfiles, "extraction looks broken"
    assert any("COPY . ." in d.read_text() for d in dockerfiles)
    ignored = (target / ".dockerignore").read_text().splitlines()
    assert ".env" in ignored


def test_every_generated_dockerfile_is_built_by_compose(tmp_path: Path) -> None:
    # A Dockerfile nothing builds is a second copy that rots out of sync with the first.
    target = tmp_path / "app"
    _run(str(target))
    compose = (target / "docker-compose.yml").read_text()
    dockerfiles = sorted(d.relative_to(target).as_posix() for d in target.rglob("Dockerfile"))
    assert len(dockerfiles) >= 2, "extraction looks broken"
    for rel in dockerfiles:
        assert rel == "Dockerfile" or f"dockerfile: {rel}" in compose, rel


def test_project_name_is_the_target_directory_everywhere_it_appears(tmp_path: Path) -> None:
    # One name, three homes (README title, package name, API title): they must agree.
    target = tmp_path / "my-rag-service"
    _run(str(target))
    assert (target / "README.md").read_text().splitlines()[0] == "# my-rag-service"
    assert 'name = "my-rag-service"' in (target / "pyproject.toml").read_text()
    assert 'FastAPI(title="my-rag-service"' in (target / "app" / "main.py").read_text()
    leftovers = [
        p.relative_to(target).as_posix()
        for p in target.rglob("*")
        if p.is_file() and "production-ai-app" in p.read_text(encoding="utf-8")
    ]
    assert leftovers == []


def test_project_name_is_made_a_valid_package_name(tmp_path: Path) -> None:
    target = tmp_path / "My RAG app!"
    _run(str(target))
    assert 'name = "My-RAG-app"' in (target / "pyproject.toml").read_text()
    assert (target / "README.md").read_text().splitlines()[0] == "# My-RAG-app"


def test_project_name_falls_back_when_the_directory_has_none() -> None:
    # A filesystem root has an empty name; a name with no usable character sanitises to "".
    sys.path.insert(0, str(SCAFFOLD.parent))
    try:
        import scaffold
    finally:
        sys.path.pop(0)
    assert scaffold.project_name(Path("/")) == "production-ai-app"
    assert scaffold.project_name(Path("/tmp/!!!")) == "production-ai-app"
    assert scaffold.project_name(Path("/tmp/my-rag-service")) == "my-rag-service"


def test_generated_linter_is_pinned(tmp_path: Path) -> None:
    # The generated lint config selects whole rule families, so a new ruff release can add
    # rules: an unpinned ruff would fail a freshly scaffolded app's first CI run.
    target = tmp_path / "app"
    _run(str(target))
    requirements = (target / "requirements.txt").read_text().splitlines()
    ruff = [line for line in requirements if line.startswith("ruff")]
    assert len(ruff) == 1 and re.fullmatch(r"ruff==\d+\.\d+\.\d+", ruff[0]), ruff
    assert "package-ecosystem: pip" in (target / ".github" / "dependabot.yml").read_text()


def test_generated_app_passes_its_own_linter(tmp_path: Path) -> None:
    # The generated pyproject encodes the same style standard as this repo; the stubs meet it.
    target = tmp_path / "app"
    _run(str(target))
    config = (target / "pyproject.toml").read_text()
    assert '"D"' in config, "the generated lint config no longer selects docstring rules"
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "--no-cache", "."],
        cwd=target, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_generated_workflow_pins_actions_and_lints(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    workflow = (target / ".github" / "workflows" / "ci.yml").read_text()
    uses = re.findall(r"uses:\s*(\S+)", workflow)
    assert len(uses) >= 2, "extraction looks broken"
    for action in uses:
        assert re.fullmatch(r"[\w./-]+@[0-9a-f]{40}", action), f"not pinned to a SHA: {action}"
    assert "ruff check" in workflow
    assert "github-actions" in (target / ".github" / "dependabot.yml").read_text()


def test_model_default_lives_in_one_place(tmp_path: Path) -> None:
    # A value in more than one place rots out of sync: config.py is the model default's home.
    target = tmp_path / "app"
    _run(str(target))
    match = re.search(r'llm_model: str = "([^"]+)"', (target / "app" / "config.py").read_text())
    assert match, "extraction looks broken"
    holders = [
        p.relative_to(target).as_posix()
        for p in target.rglob("*")
        if p.is_file() and match.group(1) in p.read_text(encoding="utf-8")
    ]
    assert holders == ["app/config.py"]


def test_config_rejects_unknown_keys_and_tests_are_not_all_skipped(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    assert 'extra="forbid"' in (target / "app" / "config.py").read_text()
    tests = sorted((target / "tests").glob("test_*.py"))
    assert len(tests) >= 5, "extraction looks broken"
    assert any("pytest.mark.skip" not in t.read_text() for t in tests)


def test_api_reference_describes_what_health_returns(tmp_path: Path) -> None:
    target = tmp_path / "app"
    _run(str(target))
    assert '"env": settings.app_env' in (target / "app" / "main.py").read_text()
    assert '"env"' in (target / "api-reference.md").read_text()
