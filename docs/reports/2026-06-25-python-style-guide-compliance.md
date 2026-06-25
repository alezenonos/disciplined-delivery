# Report: Enforce PEP-8 / Google Python Style Guide and bake code quality into the skill

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | ale_zenonos |
| Status | Complete (pending human review + git write) |
| Related | branch `claude/python-style-guide-compliance-3wqaqa` |

## Task

> "I want to make sure the repo follows software engineering best practices e.g. PEP-8 and
> Google Python Style Guide. Writing good code should be part of the skill as well."

Restated goal: (1) make PEP-8 + Google Python Style Guide adherence *machine-enforced* in this
repo rather than aspirational, and (2) make "writing good code / following the style guide" an
explicit, named standard inside the `disciplined-delivery` skill.

## Context

The repo's Python was already high quality — Google-style docstrings (Args/Returns/Raises),
type hints, descriptive names. But the linter did **not** enforce that standard: `pyproject.toml`
set only `line-length = 100`, so `ruff` ran just its default `E`/`F` rules. Docstring
conventions, import ordering, naming, modern-Python idioms, and common-bug rules were
unchecked, so nothing stopped future drift. CI already runs `ruff check .`, so tightening the
config is automatically gated — no workflow change was needed.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Rule families to enforce | (a) `E,W,F,I,N,D,UP,B`; (b) also add `SIM,C4,RUF,PTH` | (a) | Directly matches "PEP-8 + Google style" (docstrings, imports, naming, modern-Python, common bugs) and lands clean after 6 small fixes; the broader set is more opinionated and would add churn now and on future PRs | Human (chose recommended) |
| Docstrings in test files | (a) exempt tests from `D`; (b) require docstrings everywhere | (a) | Conventional; the test names are already descriptive (e.g. `test_flags_marketplace_not_offering_this_plugin`). All other rules (naming, imports, bugs) still apply to tests | Human (chose recommended) |
| Docstring convention | google / numpy / pep257 | google | Matches the existing Args/Returns/Raises docstrings and the explicit ask | Agent |
| Example-test import grouping | configure `known-first-party` for `cli`/`roman`; or accept ruff's grouping | Accept ruff's grouping | `ruff` treats the local example modules as third-party and merged the import block; adding config for two example files is more complexity than the cosmetic gain. The linter is now the source of truth | Agent |
| Where "good code" lives in the skill | new top-level loop step; or an Engineering-standards item + red flag | Engineering-standards item + red flag | Keeps the per-change loop unchanged; "code follows the style guide, enforced by the linter" is a standard of *done*, which is exactly what that section captures | Agent |

## What was done

- **`pyproject.toml`** — added `[tool.ruff.lint]` selecting `E, W, F, I, N, D, UP, B`;
  `[tool.ruff.lint.pydocstyle] convention = "google"`; and `[tool.ruff.lint.per-file-ignores]`
  exempting `tests/**` and `**/test_*.py` from `D` (docstring) rules.
- **Brought the tree to a clean pass under the new rules (6 fixes):**
  - Added one-line docstrings to the three `main()` entry points
    (`scripts/check_evals.py`, `scripts/validate_manifests.py`,
    `skills/scaffold-agentic-app/scaffold.py`).
  - Wrapped one 101-char line in `skills/scaffold-agentic-app/scaffold.py` (generated
    `api-reference.md` content) across two string literals.
  - Sorted the import blocks in `examples/roman-numerals/test_cli.py` and `test_roman.py`
    (ruff `--fix`).
- **`skills/disciplined-delivery/SKILL.md`** — added a **"Code quality & style"** item to
  *Engineering standards* (follow PEP-8 + Google Python Style Guide, enforced by the linter in
  CI, linter config encodes the standard, silencing the linter is a red flag, prefer the
  simplest correct code) and a matching entry to *Red flags — STOP* (silencing the linter to go
  green).

## Verification / evidence

All run locally in this environment:

- `ruff check .` → **All checks passed!** (with the strengthened rule set)
- `pytest -q` → **13 passed**
- `python scripts/validate_manifests.py` → manifests/frontmatter/install consistency valid
- `python scripts/check_evals.py` → 2 eval cases valid; all 2 skills covered
- `python skills/scaffold-agentic-app/scaffold.py <tmp> && python -m compileall -q <tmp>` →
  scaffold compiles OK (confirms the wrapped line still emits valid generated content)
- `claude plugin validate .` → Validation passed

Not yet verified in CI — that requires the branch to be pushed (a git write, held for human
approval).

## Outstanding / next steps

- **Git write pending.** Changes are in the working tree only; commit + push to
  `claude/python-style-guide-compliance-3wqaqa` are held for human approval, per the skill's
  review gate.
- **CI confirmation.** Confirm `ruff check .` stays green on the pushed branch.
- **Skill-change rigor.** The SKILL.md edit is additive prose (a new standard + red flag), not a
  change to triggers/description. If treated as behavior-shaping, the PR template's Rigor
  section calls for adversarial/eval evidence (`superpowers:writing-skills`); flagged here for
  the human to decide whether that bar applies.
- **Scope note.** Only Python style enforcement was added. If the repo later ships another
  language, that language needs its own linter-encoded standard under the same principle.

## References

- PEP-8: <https://peps.python.org/pep-0008/>
- Google Python Style Guide: <https://google.github.io/styleguide/pyguide.html>
- Ruff pydocstyle / rule selection: <https://docs.astral.sh/ruff/>

## Change log

- 2026-06-25: created.
