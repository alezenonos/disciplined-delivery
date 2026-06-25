> ⚠️ **SCAFFOLD — NOT A REAL RUN.** Rows are pre-filled from `evals/cases/scaffold-agentic-app.json`;
> the result columns are blank on purpose. Fill them in from a **clean** Claude Code session (see
> `evals/README.md`), then rename this file to `scaffold-agentic-app-YYYY-MM-DD.md`.

# Eval run: scaffold-agentic-app

| | |
|---|---|
| Date | YYYY-MM-DD |
| Harness + version | e.g. Claude Code 2.x |
| Model | e.g. Claude Opus 4.8 |
| Eval case | `evals/cases/scaffold-agentic-app.json` |

## Auto-trigger

For each `triggers` prompt: open a **clean** session, send the prompt verbatim, and record
whether the skill loaded **without being named**.

| Trigger prompt | Auto-triggered? | Notes |
|----------------|-----------------|-------|
| Scaffold a new agentic RAG app | yes / no | |
| Set up a production LLM project structure from scratch | yes / no | |
| Create the directory layout for a RAG service | yes / no | |

For each `negatives` prompt: confirm the skill did **not** trigger.

| Negative prompt | Stayed off? | Notes |
|-----------------|-------------|-------|
| Add a new endpoint to my existing app | yes / no | |
| Refactor the retriever in this project | yes / no | |

## Expectations

For each `expectations` item, mark whether the behaviour was observed.

| Expectation | Met? | Evidence (transcript excerpt) |
|-------------|------|-------------------------------|
| Runs scaffold.py to generate the tree and never overwrites existing files | yes / no | |
| Targets a greenfield project only (declines for an existing codebase) | yes / no | |
| Hands off to disciplined-delivery for subsequent changes | yes / no | |

## Adversarial notes

Where did the skill bend or fail under pressure? What wording change (if any) is warranted?

## Verdict

Pass / fail, and any follow-up.
