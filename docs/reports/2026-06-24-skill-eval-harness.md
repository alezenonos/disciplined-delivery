# Report: Skill-behavior eval harness

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | PR D (last of four follow-ups), after PRs #5/#6/#8/#9 merged |

## Task

Close the one standard still without a gate: skills are behavior-shaping code, but there was no
harness for auto-trigger / adversarial evals. Also update README + docs for the latest changes.

## Decision: gate the cases, run the sessions manually

A true auto-trigger eval needs a live Claude Code session + model loading a skill from its
`description` — not runnable in hermetic CI. So this delivers a **harness**, not a fully
automated gate:

- **CI gates the cases** (well-formed + every skill covered) — concrete and verifiable.
- **Humans/agents run the sessions** and commit a transcript — the evidence the PR template
  already asks for on skill changes.

I deliberately did **not** fabricate transcripts; `evals/transcripts/` ships a template only.

## What was done

- `evals/cases/<skill>.json` for both skills — the prompts that should auto-trigger, the ones
  that shouldn't, and the behaviours to verify.
- `evals/README.md` (methodology + run procedure) and `evals/transcripts/_TEMPLATE.md`.
- `scripts/check_evals.py` — hermetic validator: case files well-formed + **every skill has a
  case** (a new skill with no coverage fails CI). Wired into the CI manifests job.
- `tests/test_check_evals.py` — 3 tests (passes here; malformed case; uncovered skill). 10 total.
- Pointers added: PR template and `CONTRIBUTING.md` reference `evals/`.
- Docs synced: README gains an "Evaluating skills" section + `check_evals.py` in the
  reproduce-CI list + Layout entry; `CHANGELOG.md` Unreleased now records the post-0.1.0 work
  (eval harness, install-consistency check, CI matrix/SHA-pin/dependabot).

## Verification / evidence

`ruff` clean; `pytest -q` → 10 passed; `check_evals.py` → 2 cases valid, both skills covered;
`validate_manifests.py` + `claude plugin validate` pass; `ci.yml` parses.

**Not done (honest):** no live auto-trigger transcripts committed yet — that requires running the
cases in a clean session, which is the manual step the harness now structures.

## Outstanding / next steps

- Run the eval cases for both skills in a clean session and commit the transcripts (closes the
  long-standing auto-trigger/adversarial-evidence gap).
- Optional Dependabot policy tweak (group bumps / constrain majors) — still on offer, kept out
  of this PR to stay focused.

## Change log

- 2026-06-24: created.
