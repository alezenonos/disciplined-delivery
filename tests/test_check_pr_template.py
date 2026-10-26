"""Tests for the shipped PR-description checker (`assets/check_pr_template.py`).

Runs the script as a subprocess, the way a CI workflow invokes it (``PR_BODY`` in the
environment), against both the consumer template the plugin ships and this repo's own
template, and asserts the exit code and the reported problems.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / "skills" / "disciplined-delivery" / "assets"
CHECKER = ASSETS / "check_pr_template.py"
CONSUMER_TEMPLATE = ASSETS / "PULL_REQUEST_TEMPLATE.md"
OWN_TEMPLATE = REPO / ".github" / "PULL_REQUEST_TEMPLATE.md"

COMPLIANT_BODY = """\
## What problem does this PR solve?
PR descriptions were not enforced, so PRs could merge without the template.

## What does this PR change?
Adds a CI check that validates the PR description against the template.

## How was it tested?
New tests (red-first), 9 passing on a clean checkout of abc1234; ruff clean.

## Alternatives considered
A bot comment instead of a failing check: rejected, it does not block merge.

## Known limits
Does not check that the prose is true, only that it is there.

## Single focused change?
- [x] This PR is one self-contained change (not several unrelated ones)
- Related PRs/issues: none

## Review
- [ ] A human has reviewed the complete diff before merge
"""


def _run(body: str, *args: str, template: Path = CONSUMER_TEMPLATE) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--template", str(template), *args],
        env={**os.environ, "PR_BODY": body},
        capture_output=True,
        text=True,
    )


def _filled(template: Path) -> str:
    """A body that follows ``template``: every section present, prose written, boxes ticked."""
    text = re.sub(r"<!--.*?-->", "", template.read_text(encoding="utf-8"), flags=re.DOTALL)
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append(line)
            out.append("Filled in by the author.")
        else:
            out.append(line.replace("- [ ]", "- [x]"))
    return "\n".join(out) + "\n"


def test_compliant_body_passes() -> None:
    result = _run(COMPLIANT_BODY, "--must-tick", "Single focused change?")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "follows" in result.stdout


def test_empty_body_fails() -> None:
    result = _run("")
    assert result.returncode == 1
    assert "empty" in result.stdout.lower()


def test_raw_unfilled_consumer_template_fails() -> None:
    # The template as-is (guidance comments, unticked boxes) must NOT pass.
    result = _run(CONSUMER_TEMPLATE.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert "::error::" in result.stdout


def test_missing_section_fails() -> None:
    body = COMPLIANT_BODY.replace("## How was it tested?", "## How tested")
    result = _run(body)
    assert result.returncode == 1
    assert "Missing required section: '## How was it tested?'" in result.stdout


def test_section_left_as_guidance_comment_fails() -> None:
    body = COMPLIANT_BODY.replace(
        "Adds a CI check that validates the PR description against the template.",
        "<!-- 1-3 sentences. What, not why. -->",
    )
    result = _run(body)
    assert result.returncode == 1
    assert "'## What does this PR change?' is empty" in result.stdout


def test_unticked_must_tick_checkbox_fails() -> None:
    body = COMPLIANT_BODY.replace(
        "- [x] This PR is one self-contained change",
        "- [ ] This PR is one self-contained change",
    )
    result = _run(body, "--must-tick", "Single focused change?")
    assert result.returncode == 1
    assert "'## Single focused change?' must have its checkbox ticked" in result.stdout


def test_checkbox_sections_are_not_required_to_be_ticked_unless_named() -> None:
    # "Review" is ticked by the human during review, not when the PR is opened.
    result = _run(COMPLIANT_BODY)
    assert result.returncode == 0, result.stdout


def test_must_tick_section_absent_from_template_is_a_config_error() -> None:
    # Fail fast on config: a typo in the workflow must not silently check nothing.
    result = _run(COMPLIANT_BODY, "--must-tick", "Single focussed change?")
    assert result.returncode == 1
    assert "not a section of the template" in result.stdout


def test_rules_are_derived_from_the_template_not_hardcoded(tmp_path: Path) -> None:
    template = tmp_path / "PULL_REQUEST_TEMPLATE.md"
    template.write_text("## Why?\n<!-- say why -->\n\n## Checklist\n- [ ] done\n", encoding="utf-8")
    ok = _run("## Why?\nBecause.\n\n## Checklist\n- [ ] done\n", template=template)
    assert ok.returncode == 0, ok.stdout
    missing = _run("## Why?\nBecause.\n", template=template)
    assert missing.returncode == 1
    assert "Missing required section: '## Checklist'" in missing.stdout


def test_body_can_be_read_from_a_file(tmp_path: Path) -> None:
    body = tmp_path / "body.md"
    body.write_text(COMPLIANT_BODY, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--template", str(CONSUMER_TEMPLATE),
         "--body-file", str(body)],
        env={k: v for k, v in os.environ.items() if k != "PR_BODY"},
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_this_repos_own_template_is_enforced_the_same_way() -> None:
    # Dogfood: the plugin repo runs the shipped checker over its own template.
    raw = _run(OWN_TEMPLATE.read_text(encoding="utf-8"), template=OWN_TEMPLATE)
    assert raw.returncode == 1, raw.stdout
    filled = _run(_filled(OWN_TEMPLATE), "--must-tick", "Existing PRs", template=OWN_TEMPLATE)
    assert filled.returncode == 0, filled.stdout


def test_consumer_template_filled_in_passes_with_the_shipped_workflow_flags() -> None:
    filled = _run(_filled(CONSUMER_TEMPLATE), "--must-tick", "Single focused change?")
    assert filled.returncode == 0, filled.stdout
