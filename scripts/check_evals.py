#!/usr/bin/env python3
"""Validate the skill evaluation cases under ``evals/cases/``.

Each skill declares, as data, the prompts that should auto-trigger it, prompts
that should not, and the behaviours to verify in a run. Executing the cases
against a live session is manual (see ``evals/README.md``) — this script is the
hermetic gate that keeps the cases well-formed and ensures **every skill has an
eval case** (a new skill with no coverage fails CI).

Exit code is ``0`` when all cases are valid and every skill is covered, ``1``
otherwise. Usage: ``python scripts/check_evals.py [repo_root]``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_KEYS = ("skill", "triggers", "negatives", "expectations")
NON_EMPTY_LISTS = ("triggers", "expectations")


def _check_case(path: Path, skills: set[str], errors: list[str]) -> str | None:
    """Validate one case file; return the skill it covers (or ``None``)."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"{path}: missing key '{key}'")
    skill = data.get("skill")
    if skill and skill not in skills:
        errors.append(f"{path}: 'skill' {skill!r} has no matching skills/{skill}/SKILL.md")
    for key in NON_EMPTY_LISTS:
        val = data.get(key)
        if val is not None and (not isinstance(val, list) or not val):
            errors.append(f"{path}: '{key}' must be a non-empty list")
    return skill if isinstance(skill, str) else None


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors: list[str] = []

    skills = {p.parent.name for p in root.glob("skills/*/SKILL.md")}
    case_files = sorted((root / "evals" / "cases").glob("*.json"))
    covered = {skill for cf in case_files if (skill := _check_case(cf, skills, errors))}

    for skill in sorted(skills - covered):
        errors.append(f"skill '{skill}' has no eval case in evals/cases/")

    if errors:
        print(f"✗ {len(errors)} eval-case error(s):")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"✓ {len(case_files)} eval case(s) valid; all {len(skills)} skill(s) covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
