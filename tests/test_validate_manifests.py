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


def test_flags_install_docs_not_adding_dependency_marketplace(tmp_path: Path) -> None:
    # The 0.2.2 drift: plugin.json moved superpowers to claude-plugins-official, but
    # install.sh and the README kept adding the legacy marketplace.
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    (tmp_path / "install.sh").write_text(
        "claude plugin marketplace add obra/superpowers-marketplace\n"
    )
    (tmp_path / "README.md").write_text(
        "/plugin marketplace add obra/superpowers-marketplace\n"
    )

    result = _run(tmp_path)
    assert result.returncode == 1
    assert "install.sh never adds marketplace 'claude-plugins-official'" in result.stdout
    assert "README.md never adds marketplace 'claude-plugins-official'" in result.stdout


def test_skips_install_docs_check_when_files_absent(tmp_path: Path) -> None:
    # A consuming layout without install.sh/README is not an error for this check.
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    skill = tmp_path / "skills" / "ok" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("---\nname: ok\ndescription: ok\n---\n")

    result = _run(tmp_path)
    assert result.returncode == 0, result.stdout


def test_reports_only_the_install_doc_that_is_wrong(tmp_path: Path) -> None:
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    (tmp_path / "install.sh").write_text(
        "claude plugin marketplace add anthropics/claude-plugins-official\n"
    )
    (tmp_path / "README.md").write_text("no marketplace steps here\n")

    result = _run(tmp_path)
    assert "README.md never adds marketplace 'claude-plugins-official'" in result.stdout
    assert "install.sh never adds" not in result.stdout


def test_commented_out_marketplace_add_does_not_count(tmp_path: Path) -> None:
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    (tmp_path / "install.sh").write_text(
        "# claude plugin marketplace add anthropics/claude-plugins-official\n"
    )

    result = _run(tmp_path)
    assert "install.sh never adds marketplace 'claude-plugins-official'" in result.stdout


def test_copilot_marketplace_add_does_not_count_for_claude_code(tmp_path: Path) -> None:
    # The README's Copilot section adds obra's marketplace with `copilot plugin ...`.
    # That must not satisfy a Claude Code dependency on the same marketplace, or the
    # README's Claude Code steps can drift unnoticed (as they did after #31).
    shutil.copytree(REPO / ".claude-plugin", tmp_path / ".claude-plugin")
    plugin_json = tmp_path / ".claude-plugin" / "plugin.json"
    plugin = json.loads(plugin_json.read_text())
    plugin["dependencies"] = [{"name": "superpowers", "marketplace": "superpowers-marketplace"}]
    plugin_json.write_text(json.dumps(plugin))
    market_json = tmp_path / ".claude-plugin" / "marketplace.json"
    market = json.loads(market_json.read_text())
    market["allowCrossMarketplaceDependenciesOn"] = ["superpowers-marketplace"]
    market_json.write_text(json.dumps(market))
    (tmp_path / "install.sh").write_text(
        "claude plugin marketplace add obra/superpowers-marketplace\n"
    )
    (tmp_path / "README.md").write_text(
        "/plugin marketplace add anthropics/claude-plugins-official\n"
        "copilot plugin marketplace add obra/superpowers-marketplace\n"
    )

    result = _run(tmp_path)
    assert "README.md never adds marketplace 'superpowers-marketplace'" in result.stdout
    assert "install.sh never adds" not in result.stdout
