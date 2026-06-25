# Report: Scaffolder appends to existing CLAUDE.md/AGENTS.md instead of clobbering

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | "our skill shouldn't replace CLAUDE.md if it exists — append/edit instead" |

## Task

The scaffolder must not replace a project's existing `CLAUDE.md`; it should append/edit. (Prior
behaviour: `scaffold.py` skipped any existing file, so an existing `CLAUDE.md` was left untouched
and the scaffold's guidance was *not* added.)

## What was done (TDD)

- `scaffold.py`: project-memory files (`CLAUDE.md`, `AGENTS.md`) are now handled specially —
  - absent → created with the block wrapped in `<!-- BEGIN/END scaffold-agentic-app -->` markers;
  - present **with** our marker → skipped (already merged);
  - present **without** our marker → our block is **appended** (original content preserved).
  - The summary now reports `appended to: N`.
- Tests first: `tests/test_scaffold.py` gains 3 cases — append-without-clobber, append
  idempotency (no duplicate block on re-run), and fresh-file-carries-marker.
- Docs: module docstring + `scaffold-agentic-app/SKILL.md` note the exception; CHANGELOG
  Unreleased records it.

## Decisions

| Decision | Chosen | Why |
|----------|--------|-----|
| Which files | `CLAUDE.md` **and** `AGENTS.md` | Both are project/agent memory; same clobber risk |
| Merge style | Append a marker-delimited block | Simple, idempotent, never touches the project's own lines |
| Idempotency | Detect `BEGIN` marker → skip | Re-runs don't duplicate; markers also added on fresh create |

## Verification / evidence

`ruff` clean; `pytest -q` → **13 passed** (3 new); smoke test on a pre-existing `CLAUDE.md`:
`created: 57, appended to: 1`, original line preserved, block under markers; re-run →
`appended to: 0`, marker count 1. `validate_manifests` + `check_evals` + `claude plugin
validate` green.

## Outstanding / next steps (the other "outstanding items")

- **Eval transcripts** — needs a clean Claude Code session; can't be produced honestly from here.
- **`allowed-tools` on skills** — a behavior-shaping skill change; per our own rule it needs an
  eval run, so it's gated on the transcripts above.
- **Community-marketplace submission** — an external form (claude.ai / Console) tied to the
  maintainer's account/org; the repo is `claude plugin validate`-clean and ready to submit.
- **`v0.2.0` tag** — created locally but the session's git proxy returns 403 on tag refs (org
  policy); cut it from a normal environment (`git push origin disciplined-delivery--v0.2.0`).

## Change log

- 2026-06-25: created.
