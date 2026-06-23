<!--
Copy this file to docs/reports/YYYY-MM-DD-<slug>.md and fill it in.
One report per Claude task. More elaborate than the PR description: it
captures the reasoning and the handoff, not just the diff. Be honest —
claim only what was actually run, and be explicit about what is NOT done.
-->

# Report: <short title>

| | |
|---|---|
| Date created | YYYY-MM-DD |
| Last edited | YYYY-MM-DD |
| Author | <agent + version, e.g. Claude Opus 4.8 (Claude Code)> |
| Human partner | <name> |
| Status | In progress \| Complete \| Blocked |
| Related | PR #, branch, key commits |

## Task

What the human asked, in their words (quote/paraphrase), plus a one-line restatement of the
goal as understood.

## Context

The starting state and the background a collaborator needs to understand the task. What
existed before; what problem or need prompted this.

## Decisions

The load-bearing decisions. For each: the question, the options considered, what was chosen,
**why**, and **who decided** (human vs agent). This is the part the PR description does not
capture — make it the most elaborate section.

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
|          |         |        |     |            |

## What was done

The concrete changes, grouped logically, referencing files and commits. What, not why (the
why is above).

## Verification / evidence

Exactly what was run and the result. Claim only what was actually executed. Distinguish
"verified locally" from "verified in CI / production".

## Outstanding / next steps

Honest list of what is NOT done, known gaps, risks, and what a collaborator should pick up
next — enough that someone else can continue without re-deriving context. Flag any decisions
still owed by the human.

## References

Links: PRs, issues, docs, external sources used.

## Change log

- YYYY-MM-DD: created.
