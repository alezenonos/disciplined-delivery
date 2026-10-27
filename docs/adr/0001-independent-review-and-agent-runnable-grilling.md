---
status: accepted
---

# The pre-PR review is independent, and the grilling step is one the agent can start

The pre-PR review gate is an **independent reviewer that sees only the branch's diff, never the
author's session**. The skill names it by that role, not by a tool. In Claude Code the
default is the built-in `/code-review`; elsewhere it is `superpowers:requesting-code-review`, which
dispatches a fresh reviewer subagent and is already a dependency. The awesome-skills
`code-review-skill` is no longer a companion. "Think first" grills load-bearing decisions with
**`grilling` plus `domain-modeling`** instead of `grill-with-docs`. `grill-with-docs` is only those
two skills combined, but it sets `disable-model-invocation: true`, so an agent told to use it
cannot start it.

Decided by the maintainer on 2026-10-27, one question at a time. The evidence: on the same day's
diffs, a self-review with `code-review-skill` found 3 issues, and an independent `/code-review`
found 9 on the same change, including the one structural fix. In a baseline run of the old wording,
3 of 3 agents reviewed their own work and said the skill did not call for an independent reviewer.

## Considered Options

- **Keep `code-review-skill` as the gate.** Rejected: it is a checklist the author runs on their
  own work, so the review is anchored on the author's reasoning, and it was a separate `git clone`
  install with drift across three documented paths.
- **Require `superpowers:requesting-code-review` everywhere.** Rejected as the Claude Code default:
  unmeasured on a real diff here, while `/code-review` is built in and was measured.
- **Require a specific tool per agent.** Rejected: naming the role, not the tool, survives tools
  changing, which is how the old companion went stale.
- **Have the agent ask the human to type `/grill-with-docs`.** Rejected: it makes the human the
  trigger for a step the agent should start.
- **Drop the grilling companion for `superpowers:brainstorming` alone.** Rejected: brainstorming
  explores options; grilling resolves one decision at a time and records it.

## Consequences

`code-review-skill` stays installable by anyone who wants it; the plugin stops recommending it.
Companion installs become one command (`npx skills@latest add mattpocock/skills`, selecting
`grilling` and `domain-modeling`).
