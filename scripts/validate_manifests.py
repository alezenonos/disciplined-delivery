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
import re
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


README_MARKERS = ("<!-- install-check: claude-code -->", "<!-- /install-check -->")


def _check_install_docs_add(
    root: Path, dep_name: str | None, dep_market: str, errors: list[str]
) -> None:
    """Require each install doc to add ``<owner>/<dep_market>`` before installing the plugin.

    ``plugin.json`` dependencies are resolved by Claude Code, so only its
    install steps count: all of ``install.sh``, and in ``README.md`` only the
    section between ``README_MARKERS``, so another agent's steps (Copilot's)
    can't satisfy it. A marketplace's name is matched against the repo name in
    the argument, which holds for GitHub-hosted marketplaces such as
    ``anthropics/claude-plugins-official``. Only a line that starts with the
    command counts, so a comment, an ``echo`` or prose that mentions it doesn't.
    """
    command = r"^[ \t]*(?:/plugin|claude plugin) "
    adds = re.compile(
        rf"{command}marketplace add\s+[\w.-]+/{re.escape(dep_market)}(?![\w.-])", re.MULTILINE
    )
    installs = re.compile(rf"{command}install\b", re.MULTILINE)
    for doc in ("install.sh", "README.md"):
        path = root / doc
        if not path.is_file():
            continue
        steps = path.read_text(encoding="utf-8")
        if doc == "README.md":
            start, end = README_MARKERS
            # Exactly one of each, in order: a quoted or stray marker must not widen the section.
            one_each = steps.count(start) == 1 and steps.count(end) == 1
            if not one_each or steps.find(end) < steps.find(start):
                errors.append(
                    f"install: README.md has no '{start}' … '{end}' section around its "
                    "Claude Code install steps"
                )
                continue
            steps = steps.split(start, 1)[1].split(end, 1)[0]
        add = adds.search(steps)
        install = installs.search(steps)
        if add is None:
            errors.append(
                f"install: {doc} never adds marketplace '{dep_market}', which dependency "
                f"'{dep_name}' resolves from — a fresh install would leave it unresolved"
            )
        elif install is not None and install.start() < add.start():
            errors.append(
                f"install: {doc} installs the plugin before adding marketplace "
                f"'{dep_market}', so dependency '{dep_name}' would be left unresolved"
            )


def validate_install_consistency(root: Path, errors: list[str]) -> None:
    """Cross-check the manifests so a fresh install actually resolves.

    A hermetic stand-in for a live install smoke test (which needs the Claude
    Code CLI + network). Catches the common install-breakers:

    1. a cross-marketplace dependency that isn't allow-listed,
    2. a self-hosting marketplace that doesn't actually offer this plugin, and
    3. install instructions that never add the marketplace a dependency
       resolves from, or add it only after installing the plugin, so a fresh
       install leaves it unresolved. Checked in ``install.sh`` and in
       ``README.md``'s Claude Code steps, which must sit between exactly one
       pair of ``README_MARKERS``; a file that doesn't exist is skipped.
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
        if dep_market and dep_market != market_name:
            _check_install_docs_add(root, dep.get("name"), dep_market, errors)

    plugin_name = plugin.get("name")
    offered = {e.get("name") for e in market.get("plugins", []) if isinstance(e, dict)}
    if plugin_name and plugin_name not in offered:
        errors.append(
            f"install: marketplace.json offers {sorted(n for n in offered if n)}, not this "
            f"plugin '{plugin_name}' — it could not be installed from its own marketplace"
        )


def main(argv: list[str]) -> int:
    """Validate all manifests and return ``0`` if they are consistent, else ``1``."""
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
