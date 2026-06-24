<!-- Copy to evals/transcripts/<skill>-YYYY-MM-DD.md and fill in from a real run. -->

# Eval run: <skill>

| | |
|---|---|
| Date | YYYY-MM-DD |
| Harness + version | e.g. Claude Code 2.x |
| Model | e.g. Claude Opus 4.8 |
| Eval case | `evals/cases/<skill>.json` |

## Auto-trigger

For each `triggers` prompt: open a **clean** session, send the prompt verbatim, and record
whether the skill loaded **without being named**.

| Trigger prompt | Auto-triggered? | Notes |
|----------------|-----------------|-------|
| ...            | yes / no        |       |

For each `negatives` prompt: confirm the skill did **not** trigger.

| Negative prompt | Stayed off? | Notes |
|-----------------|-------------|-------|
| ...             | yes / no    |       |

## Expectations

For each `expectations` item, mark whether the behaviour was observed.

| Expectation | Met? | Evidence (transcript excerpt) |
|-------------|------|-------------------------------|
| ...         | yes / no | |

## Adversarial notes

Where did the skill bend or fail under pressure? What wording change (if any) is warranted?

## Verdict

Pass / fail, and any follow-up.
