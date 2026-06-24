"""Tests for the scaffold-agentic-app generator (`scaffold.py`).

Characterization tests: the generator already exists, so these pin its current
contract — produces the expected tree, the output compiles, and re-running is
idempotent (never overwrites).
"""
from __future__ import annotations

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
    ".github/workflows/ci.yml",
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
