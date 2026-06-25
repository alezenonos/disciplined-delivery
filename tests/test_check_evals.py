"""Tests for `scripts/check_evals.py`.

Confirms the checker passes on this repo and fails on a malformed case and on a
skill that has no eval coverage.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "scripts" / "check_evals.py"


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(root)], capture_output=True, text=True
    )


def test_passes_on_this_repo() -> None:
    result = _run(REPO)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "all" in result.stdout and "covered" in result.stdout


def _seed_skill(root: Path, name: str) -> None:
    skill = root / "skills" / name / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(f"---\nname: {name}\ndescription: x\n---\n")


def test_fails_on_malformed_case(tmp_path: Path) -> None:
    _seed_skill(tmp_path, "demo")
    case = tmp_path / "evals" / "cases" / "demo.json"
    case.parent.mkdir(parents=True)
    case.write_text(json.dumps({"skill": "demo", "triggers": [], "negatives": []}))

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "'triggers' must be a non-empty list" in result.stdout
    assert "missing key 'expectations'" in result.stdout


def test_fails_when_skill_has_no_case(tmp_path: Path) -> None:
    _seed_skill(tmp_path, "uncovered")
    (tmp_path / "evals" / "cases").mkdir(parents=True)

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "skill 'uncovered' has no eval case" in result.stdout
