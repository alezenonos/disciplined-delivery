#!/usr/bin/env python3
"""Validate this plugin's manifests and skill frontmatter.

Run as part of CI (and locally) to catch malformed plugin/marketplace
manifests and skills that are missing the frontmatter Claude Code needs to
discover them. Uses only the standard library so CI stays hermetic.

Exit code is ``0`` when everything is valid and ``1`` when any check fails;
all failures are collected and printed, not just the first.

Usage:
    python scripts/validate_manifests.py [repo_root]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _load_json(path: Path, errors: list[str]) -> dict | None:
    """Parse a JSON file, recording a readable error instead of raising."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
    return None


def _frontmatter(path: Path) -> str | None:
    """Return the YAML frontmatter block of a Markdown file, or ``None``.

    The block is the text between the first two ``---`` fences. We avoid a
    YAML dependency and only need to confirm required keys are present.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else None


def validate_plugin(root: Path, errors: list[str]) -> None:
    """Validate ``.claude-plugin/plugin.json`` (name required, deps well-formed)."""
    data = _load_json(root / ".claude-plugin" / "plugin.json", errors)
    if data is None:
        return
    if not data.get("name"):
        errors.append("plugin.json: missing required field 'name'")
    for dep in data.get("dependencies", []):
        if isinstance(dep, dict) and not dep.get("name"):
            errors.append(f"plugin.json: dependency without a name: {dep!r}")
        elif not isinstance(dep, (str, dict)):
            errors.append(f"plugin.json: dependency must be a string or object: {dep!r}")


def validate_marketplace(root: Path, errors: list[str]) -> None:
    """Validate ``.claude-plugin/marketplace.json`` and each plugin entry."""
    data = _load_json(root / ".claude-plugin" / "marketplace.json", errors)
    if data is None:
        return
    for field in ("name", "owner", "plugins"):
        if not data.get(field):
            errors.append(f"marketplace.json: missing required field '{field}'")
    for entry in data.get("plugins", []):
        if not entry.get("name"):
            errors.append(f"marketplace.json: plugin entry missing 'name': {entry!r}")
        source = entry.get("source")
        if source is None:
            errors.append(f"marketplace.json: plugin '{entry.get('name')}' missing 'source'")
        elif isinstance(source, str) and not source.startswith("./"):
            errors.append(
                f"marketplace.json: relative source must start with './': {source!r}"
            )


def validate_skills(root: Path, errors: list[str]) -> None:
    """Every ``skills/*/SKILL.md`` must declare 'name' and 'description'."""
    skills_dir = root / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found under skills/*/SKILL.md")
    for skill in skill_files:
        fm = _frontmatter(skill)
        if fm is None:
            errors.append(f"{skill}: missing YAML frontmatter")
            continue
        for key in ("name:", "description:"):
            if key not in fm:
                errors.append(f"{skill}: frontmatter missing '{key.rstrip(':')}'")


def validate_install_consistency(root: Path, errors: list[str]) -> None:
    """Cross-check the manifests so a fresh install actually resolves.

    A hermetic stand-in for a live install smoke test (which needs the Claude
    Code CLI + network). Catches the two common install-breakers:

    1. a cross-marketplace dependency that isn't allow-listed, and
    2. a self-hosting marketplace that doesn't actually offer this plugin.
    """
    plugin = _load_json(root / ".claude-plugin" / "plugin.json", [])
    market = _load_json(root / ".claude-plugin" / "marketplace.json", [])
    if not isinstance(plugin, dict) or not isinstance(market, dict):
        return  # missing/invalid manifests are already reported by the validators above

    market_name = market.get("name")
    allowed = set(market.get("allowCrossMarketplaceDependenciesOn") or [])
    for dep in plugin.get("dependencies", []):
        if not isinstance(dep, dict):
            continue  # a bare-string dep resolves in this marketplace; nothing to cross-check
        dep_market = dep.get("marketplace")
        if dep_market and dep_market != market_name and dep_market not in allowed:
            errors.append(
                f"install: dependency '{dep.get('name')}' resolves from marketplace "
                f"'{dep_market}', not in allowCrossMarketplaceDependenciesOn "
                f"{sorted(allowed)} — cross-marketplace install would be blocked"
            )

    plugin_name = plugin.get("name")
    offered = {e.get("name") for e in market.get("plugins", []) if isinstance(e, dict)}
    if plugin_name and plugin_name not in offered:
        errors.append(
            f"install: marketplace.json offers {sorted(n for n in offered if n)}, not this "
            f"plugin '{plugin_name}' — it could not be installed from its own marketplace"
        )


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors: list[str] = []

    validate_plugin(root, errors)
    validate_marketplace(root, errors)
    validate_skills(root, errors)
    validate_install_consistency(root, errors)

    if errors:
        print(f"✗ {len(errors)} validation error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("✓ manifests, skill frontmatter, and install consistency are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
