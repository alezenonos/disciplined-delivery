# Report: Release engineering — CHANGELOG + versioning policy

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | first of four sequenced follow-up PRs (CHANGELOG, CI hardening, install smoke test, eval harness) |

## Task

Maintainer said "yes to all" four remaining follow-ups. Per the no-bundling rule, they ship as
separate focused PRs; **this is PR A: release engineering.**

## What was done

- **`CHANGELOG.md`** — Keep a Changelog format; `0.1.0` baseline documenting everything shipped
  so far, plus an `Unreleased` section and compare/release links.
- **`CONTRIBUTING.md`** — new "Releasing (maintainers)" section: semver, bump
  `plugin.json` version, tag `<plugin>--v<version>` via `claude plugin tag --push`, and add a
  changelog entry per user-facing change.
- **README** — Layout lists `CONTRIBUTING.md` + `CHANGELOG.md`.

## Decisions

| Decision | Chosen | Why |
|----------|--------|-----|
| Changelog format | Keep a Changelog + SemVer | Industry standard, tool-friendly |
| Release tag scheme | `<plugin>--v<version>` via `claude plugin tag` | The convention Claude Code uses to resolve versioned plugin dependencies |
| Bump version now? | Keep `0.1.0`; accumulate under `Unreleased` | No release cut yet; 0.1.0 is the current baseline |
| Touch the skill? | No | Avoids the "skills are code" eval requirement; keeps this PR focused on release docs |

## Verification / evidence

`ruff check .` clean, `pytest -q` → 5 passed, `validate_manifests.py` ✓, `claude plugin
validate .` ✓. (No code changed; ran the suite to confirm nothing regressed.)

## Outstanding / next steps

The remaining three follow-ups, each its own PR after this merges:
- **PR B — CI hardening:** SHA-pin `actions/*`, add a Python version matrix (3.10–3.13).
- **PR C — Install smoke test:** automate add-marketplace → install → assert `superpowers`
  resolves + skills enabled. **Caveat:** the Claude Code CLI may need auth/non-interactive
  support in CI; if it's not reliably runnable headless, fall back to a resolvability check.
- **PR D — Skill-behavior eval harness:** structure + (where feasible) automation for
  auto-trigger / adversarial evals — the one standard still without a gate.

## Change log

- 2026-06-24: created.
