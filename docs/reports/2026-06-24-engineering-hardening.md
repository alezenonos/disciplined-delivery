# Report: Adopt top engineering gaps (LICENSE, tests, lint) + why the rules lagged

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | follows the docs-audit report; branch `claude/agentic-systems-structure-qef42e` |

## Task

*"Adopt top gaps first. Then do a PR only if rules are followed. Why were they not followed to
begin with? Is the process not clear in CLAUDE.md or README? How to improve the repo so that
when it is downloaded and installed it works?"*

## What was done

Closed the top gaps from the audit:

- **`LICENSE`** — MIT (mirrors the companion skills; holder `alezenonos`).
- **`tests/`** — pytest suite for the repo's own tooling: `test_scaffold.py` (tree, compiles,
  idempotent) and `test_validate_manifests.py` (passes on this repo; fails on a broken manifest
  + frontmatter-less skill). 5 tests.
- **Lint** — `pyproject.toml` with `ruff` + `pytest` config; CI gains a **Lint & unit tests**
  job running `ruff check .`, `pytest`, and `shellcheck install.sh`.
- **Docs** — README `Layout`/`Development` updated; new **Verify your install** section;
  CLAUDE.md now states the repo dogfoods its own skill and lists `ruff`/`pytest` in the
  reproduce-CI block.

## Decisions

| Decision | Chosen | Why |
|----------|--------|-----|
| License | MIT | Matches the companion ecosystem; permissive | 
| Test style | subprocess characterization tests | Tooling already works; pin the real CLI contract without import/path hacks |
| Ruff rules | defaults + `line-length = 100` | Existing code already passes; avoid a noisy first run |
| `claude plugin validate` in CI | left out (kept as documented local + Verify step) | The Claude Code CLI isn't reliably installable/authable in CI; the stdlib validator is the hermetic gate |

## Why the rules weren't followed to begin with (root cause)

Honest analysis — it was **not** mainly a clarity problem; it was an **enforcement and
applicability** problem:

1. **The skill wasn't governing its own construction.** For most of the session I was
   *authoring* `disciplined-delivery`, not running under it. The plugin wasn't installed/active
   in this session, and `CLAUDE.md` didn't exist until partway through — so nothing surfaced the
   loop to the agent at decision time.
2. **The standards weren't mechanically enforceable.** "Tests green / linter green" was vacuous
   because the repo had **no tests and no linter** until now; CI didn't lint or unit-test the
   tooling. A rule with no gate is a suggestion.
3. **Ambiguity about scope.** The skill reads as guidance for *downstream* repos; it wasn't
   explicit that it also binds development *of this repo*. (Fixed: CLAUDE.md now says it dogfoods.)
4. **Iterative, bundled requests.** Many small asks in one session naturally bundled into large
   PRs — exactly the "one focused change" rule the skill warns about.

**Fixes applied:** real gates (lint + unit tests in CI), an explicit dogfooding statement in
CLAUDE.md, and the Verify-your-install path. Remaining: the rule with still no gate is the
**skill-behavior eval / auto-trigger transcript** requirement.

## How to make "it works when installed" trustworthy

- **Now:** CI lints, unit-tests the generator/validator, validates manifests, and runs the
  scaffold end-to-end; README has a **Verify your install** checklist (`claude plugin list`,
  companion presence, slash-command autocomplete).
- **Recommended next:** an install smoke test (add obra's marketplace → install → assert
  `superpowers` resolved + skills enabled), as done manually for PR #2 but not yet automated;
  optionally `claude plugin validate` in CI once CLI install is proven non-interactive.

## Verification / evidence

Full local CI reproduction passed: `ruff check .` clean; `pytest -q` → 5 passed;
`validate_manifests.py` ✓; `claude plugin validate .` ✓; scaffold self-test (generate, compile,
idempotent re-run) ✓.

## Outstanding / next steps

1. Push; confirm the new **Lint & unit tests** CI job is green on the branch.
2. Run the diff through `code-review-skill` (the loop's gate) before opening the PR.
3. Follow-ups (not in this change): `CONTRIBUTING.md`, `CHANGELOG` + release/versioning, CI
   action SHA-pinning + Python matrix, markdown link-check, and the skill-behavior eval harness.

## Change log

- 2026-06-24: created.
- 2026-06-24: added `CONTRIBUTING.md` (rules bind every contributor, human or agent; points to
  the skill / CLAUDE.md / PR template as single sources), linked from README and the PR template.
