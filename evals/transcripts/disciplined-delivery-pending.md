> ⚠️ **SCAFFOLD — NOT A REAL RUN.** Rows are pre-filled from `evals/cases/disciplined-delivery.json`;
> the result columns are blank on purpose. Fill them in from a **clean** Claude Code session (see
> `evals/README.md`), then rename this file to `disciplined-delivery-YYYY-MM-DD.md`.

# Eval run: disciplined-delivery

| | |
|---|---|
| Date | YYYY-MM-DD |
| Harness + version | e.g. Claude Code 2.x |
| Model | e.g. Claude Opus 4.8 |
| Eval case | `evals/cases/disciplined-delivery.json` |

## Auto-trigger

For each `triggers` prompt: open a **clean** session, send the prompt verbatim, and record
whether the skill loaded **without being named**.

| Trigger prompt | Auto-triggered? | Notes |
|----------------|-----------------|-------|
| Implement a small feature in this repo and open a PR | yes / no | |
| Fix this bug and commit the change | yes / no | |
| Add input validation to this function | yes / no | |

For each `negatives` prompt: confirm the skill did **not** trigger.

| Negative prompt | Stayed off? | Notes |
|-----------------|-------------|-------|
| What does this function return? | yes / no | |
| Explain how this module works | yes / no | |

## Expectations

For each `expectations` item, mark whether the behaviour was observed.

| Expectation | Met? | Evidence (transcript excerpt) |
|-------------|------|-------------------------------|
| Plans/brainstorms before coding for non-trivial work (via the superpowers plugin) | yes / no | |
| Writes a failing test first, then the minimal code to green (TDD) | yes / no | |
| Keeps tests + linter + CI green before claiming done | yes / no | |
| Runs code-review-skill over the diff before opening a PR | yes / no | |
| Stops and asks before any git write (branch/commit/push/PR) | yes / no | |
| Fills the PR template and leaves a docs/reports entry | yes / no | |

## Adversarial notes

Where did the skill bend or fail under pressure? What wording change (if any) is warranted?

## Verdict

Pass / fail, and any follow-up.
