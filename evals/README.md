# Skill evaluations

Skills are behavior-shaping code, so they are evaluated, not just written. This directory is
the harness:

- **`cases/<skill>.json`** — for each skill, the prompts that should **auto-trigger** it, the
  prompts that should **not**, and the **expectations** (behaviours to verify in a run).
- **`transcripts/`** — recorded runs (from `_TEMPLATE.md`), the evidence the PR template asks
  for on skill changes.
- **`../scripts/check_evals.py`** — the hermetic gate (run in CI): validates the case files and
  fails if any skill lacks a case. It does **not** run the cases — that part is manual, below.

## Why partly manual

Auto-triggering is a property of the live harness loading a skill from its `description`; it
can't be exercised in hermetic CI without a real Claude Code session and model. So CI gates the
**cases** (well-formed, full coverage) while a human/agent runs the **sessions** and commits the
transcript.

## Running an eval (per skill)

1. Open a **clean** Claude Code session (the plugin + companions installed).
2. For each `triggers` prompt in `cases/<skill>.json`, send it verbatim and confirm the skill
   loads **without being named**. For each `negatives` prompt, confirm it does **not** load.
3. Drive one trigger through to completion and check each `expectations` item.
4. **Adversarial pass:** push back, give ambiguous or "just skip it" prompts, and see whether the
   skill holds (e.g. still stops before a git write). Note where it bends.
5. Save the run as `transcripts/<skill>-YYYY-MM-DD.md` (from `_TEMPLATE.md`) and link it from the
   PR.

## Adding a skill

Add `cases/<new-skill>.json` in the same change — otherwise `check_evals.py` (and CI) fails.
