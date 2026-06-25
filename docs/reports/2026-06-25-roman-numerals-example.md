# Report: Roman-numerals worked example for `disciplined-delivery`

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | ale_zenonos@hotmail.com |
| Status | Complete (committed + pushed; code-reviewed) |
| Related | branch `claude/skill-plugin-demo-app-4nxdg7`, commit `764229b`; files under `examples/roman-numerals/` |

## Task

The human asked: *"can you do a dummy simple app that follows this skill plugin?"*

Restated goal: produce a small, simple demo app that visibly follows the
`disciplined-delivery` loop (test-first, small increment, docs, verified
green), shipped in this repo as a worked example.

## Context

This repo *is* the plugin (skills `disciplined-delivery` and
`scaffold-agentic-app`); it has no example apps. The feature branch is named
`skill-plugin-demo-app`, confirming a demo belongs on it. `scaffold-agentic-app`
exists but produces a heavyweight production RAG skeleton — the opposite of
"dummy simple" — so it was not the right tool here.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Demo type | (a) tiny hand-built TDD app, (b) run the scaffold generator, (c) both | (a) tiny TDD app | "Dummy simple" rules out the production scaffold; a small app best shows the disciplined-delivery loop | Human (via clarifying question) |
| Location | `examples/` in this repo vs. a scratch dir | `examples/` | Ships with the plugin as a reusable worked example | Human (via clarifying question) |
| The app | Roman-numeral converter vs. tip splitter / FizzBuzz | Roman numerals | Canonical TDD kata with clear red→green increments and real edge cases (range, type, subtractive pairs) | Agent |
| Test wiring | Add to repo `testpaths` vs. keep self-contained | Self-contained | Avoids mixing the demo into the plugin's own CI; surgical, no change to repo config | Agent |

## What was done

- `examples/roman-numerals/test_roman.py` — pytest suite (known values,
  out-of-range, non-int), written **before** the implementation.
- `examples/roman-numerals/roman.py` — `to_roman(number)` via a greedy pass
  over additive + subtractive numerals; validates range (1–3999) and type
  (rejects non-`int`, including `bool`).
- `examples/roman-numerals/cli.py` — thin one-argument CLI wrapper.
- `examples/roman-numerals/README.md` — how to run it and how each step mapped
  to the skill.

## Verification / evidence

All run locally on this branch:

- `python -m pytest -q` in the example dir — **23 passed**. Confirmed red first:
  before `roman.py` existed the suite failed with
  `ModuleNotFoundError: No module named 'roman'`.
- `python cli.py 1954` → `MCMLIV`; `python cli.py 4000` → `error: number must
  be in 1..3999, got 4000` (exit 2).
- `ruff check .` (whole repo) — **All checks passed**.
- Repo unaffected: `pytest -q` (repo) — 13 passed;
  `scripts/validate_manifests.py` and `scripts/check_evals.py` — both pass.

- Committed as `764229b` and pushed to `claude/skill-plugin-demo-app-4nxdg7`
  (human approved the git write). The `code-review` skill was then run over
  the diff: no correctness/cleanup findings; the only finding was this report
  being stale on commit status, fixed here.

Not yet verified in CI: pushing a feature branch does not trigger the workflow
(it runs on `push` to `main` and on `pull_request`), and no PR is open yet.

## Outstanding / next steps

- No PR has been opened (none requested). Opening one triggers the
  `pull_request` workflow and is the point at which CI gives green evidence.
- The example's tests are intentionally **not** in the repo's CI
  (`testpaths = ["tests"]`). If you want them gated, add a CI step running
  `pytest examples/roman-numerals` — flagged as a deliberate non-change.

## References

- `skills/disciplined-delivery/SKILL.md` — the loop being demonstrated.
- `examples/roman-numerals/README.md` — the example's own walkthrough.

## Change log

- 2026-06-25: created; example built test-first and verified locally, awaiting git-write approval.
- 2026-06-25: committed (`764229b`) + pushed; ran `code-review`, synced report to committed state.
