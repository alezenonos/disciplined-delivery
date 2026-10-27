#!/usr/bin/env python3
"""Validate a pull-request description against the repository's PR template.

Reads the PR body from the ``PR_BODY`` environment variable (set in CI from
``github.event.pull_request.body``) or from ``--body-file``, and exits non-zero,
printing GitHub Actions ``::error::`` annotations, if the description does not
follow the template.

The rules are read from the template, not written here, so a repository changes
what a PR must say by editing the template alone:

* every ``## `` section header of the template must be present in the body;
* a section that in the template holds nothing but HTML guidance comments is a
  **prose** section: the body must carry real content there once the comments
  are stripped (the author replaced the ``<!-- … -->`` hints);
* a section named with ``--must-tick`` must contain a ticked checkbox (``- [x]``).
  Naming a section the template does not have is a configuration error, not a
  silent no-op.

Checkbox sections not named with ``--must-tick`` are not required to be ticked
at CI time: the "Review" box is a human's to tick during review, not the
author's to tick when opening the PR.

Usage::

    check_pr_template.py [--template PATH] [--must-tick SECTION]... [--body-file PATH]

HTML comments are removed before anything is read, and a ``## `` line inside a
fenced code block (a pasted transcript or log) is content, not a header.

Kept deliberately simple and reviewable: it checks that the sections are there
and filled, not that what they say is true. A section whose template holds a
skeleton (a table, a bullet list, a ``<details>`` block) is required to be
present but its content is not checked, because an honestly unticked list looks
the same as an untouched one.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_HEADER_RE = re.compile(r"^\s*##\s+(.*?)\s*$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_TICKED_RE = re.compile(r"^\s*[-*+]\s+\[[xX]\]", re.MULTILINE)


def strip_comments(text: str) -> str:
    """Remove HTML comments (the template's guidance) from ``text``."""
    return _COMMENT_RE.sub("", text)


def parse_sections(text: str) -> dict[str, str]:
    """Split a markdown body into ``{header_title: content}`` on ``## `` headers.

    HTML comments are removed first, and lines inside fenced code blocks are never
    headers. Text before the first header (a template's preamble) is dropped; a
    title that repeats has its contents joined, so neither copy can hide the other.
    """
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        if current is not None:
            prior = sections.get(current)
            joined = "\n".join(buf)
            sections[current] = joined if prior is None else f"{prior}\n{joined}"

    for line in strip_comments(text).splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
        match = None if in_fence else _HEADER_RE.match(line)
        if match:
            flush()
            current = match.group(1).strip()
            buf = []
        else:
            buf.append(line)
    flush()
    return sections


def template_rules(template_text: str) -> tuple[list[str], list[str]]:
    """Return ``(required_sections, prose_sections)`` read from the template.

    A prose section is one whose template content is empty once the guidance
    comments are stripped: the author is expected to replace the hint with text.
    """
    sections = parse_sections(template_text)
    required = list(sections)
    prose = [title for title, body in sections.items() if not body.strip()]
    return required, prose


def validate(body: str | None, template_text: str, must_tick: list[str]) -> list[str]:
    """Return a list of problems; empty means the description is compliant."""
    required, prose = template_rules(template_text)
    problems: list[str] = []

    known = {title.lower() for title in required}
    for title in must_tick:
        if title.lower() not in known:
            problems.append(
                f"--must-tick '{title}' is not a section of the template; fix the workflow"
            )
    if problems:
        return problems

    if not body or not body.strip():
        return ["PR description is empty: fill in the PR template."]

    by_title = {title.lower(): content for title, content in parse_sections(body).items()}

    for title in required:
        if title.lower() not in by_title:
            problems.append(f"Missing required section: '## {title}'")

    for title in prose:
        content = by_title.get(title.lower())
        if content is not None and not content.strip():
            problems.append(
                f"Section '## {title}' is empty: replace the guidance comment with real content."
            )

    for title in must_tick:
        content = by_title.get(title.lower())
        if content is not None and not _TICKED_RE.search(content):
            problems.append(f"Section '## {title}' must have its checkbox ticked '- [x]'.")

    return problems


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, validate the body, print annotations; ``0`` when compliant."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--template", default=".github/PULL_REQUEST_TEMPLATE.md",
                        help="the template to validate against (default: %(default)s)")
    parser.add_argument("--must-tick", action="append", default=[], metavar="SECTION",
                        help="a section whose checkbox the author must tick; repeatable")
    parser.add_argument("--body-file", help="read the PR body from this file instead of PR_BODY")
    args = parser.parse_args(argv)

    template_path = Path(args.template)
    if not template_path.is_file():
        print(f"::error::PR template not found: {template_path}")
        return 1
    template_text = template_path.read_text(encoding="utf-8")
    body = (Path(args.body_file).read_text(encoding="utf-8") if args.body_file
            else os.environ.get("PR_BODY"))

    problems = validate(body, template_text, args.must_tick)
    if problems:
        for problem in problems:
            print(f"::error::{problem}")
        print(
            f"\nPR description does not follow {template_path}: "
            "edit the PR description to re-run this check."
        )
        return 1
    print(f"PR description follows {template_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
