"""Tests for `scripts/validate_manifests.py`.

Confirms the validator passes on this repo and fails (with useful messages) on
a broken manifest and a frontmatter-less skill.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "scripts" / "validate_manifests.py"


def _run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(root)], capture_output=True, text=True
    )


def test_passes_on_this_repo() -> None:
    result = _run(REPO)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "valid" in result.stdout


def test_fails_on_broken_manifest_and_missing_frontmatter(tmp_path: Path) -> None:
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")

    plugin_json = tmp_path / ".claude-plugin" / "plugin.json"
    data = json.loads(plugin_json.read_text())
    data.pop("name", None)
    plugin_json.write_text(json.dumps(data))

    skill = tmp_path / "skills" / "broken" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("no frontmatter here")

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "missing required field 'name'" in result.stdout
    assert "missing YAML frontmatter" in result.stdout


def test_flags_unallowlisted_cross_marketplace_dep(tmp_path: Path) -> None:
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    market = tmp_path / ".claude-plugin" / "marketplace.json"
    data = json.loads(market.read_text())
    data["allowCrossMarketplaceDependenciesOn"] = []  # drop the allowlist
    market.write_text(json.dumps(data))

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "cross-marketplace install would be blocked" in result.stdout


def test_flags_marketplace_not_offering_this_plugin(tmp_path: Path) -> None:
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    plugin_json = tmp_path / ".claude-plugin" / "plugin.json"
    data = json.loads(plugin_json.read_text())
    data["name"] = "renamed-plugin"  # marketplace no longer offers this name
    plugin_json.write_text(json.dumps(data))

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "could not be installed from its own marketplace" in result.stdout
