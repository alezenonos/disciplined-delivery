# Report: Independent pre-PR review, and a grilling step the agent can start

| | |
|---|---|
| Date created | 2026-10-27 |
| Last edited | 2026-10-27 |
| Author | Claude Opus 5.5 (Claude Code 2.1.311) |
| Human partner | alezenonos |
| Status | In progress |
| Related | branch `feat/independent-review-and-grilling`; [ADR 0001](../adr/0001-independent-review-and-agent-runnable-grilling.md); transcript `evals/transcripts/disciplined-delivery-2026-10-27-wording.md`; prior PRs #29, #30, #32 |

## Task

The human asked: *"let's revisit the use of code review by awesome skills. why not use code
review by superpowers or claude?"*, after pointing out that the agent had skipped brainstorming,
grilling and asking on #29 (*"are we following what we preach?"*). Goal: make the skill's pre-PR
review and its "think first" step ones an agent can and will actually follow.

## Context

The skill required `code-review-skill` (awesome-skills) before a PR and `grill-with-docs`
(mattpocock/skills) for load-bearing decisions. On 2026-10-27 two gaps showed:

- **The review was a self-review.** `code-review-skill` is a checklist the authoring agent runs on
  its own diff in its own session. On #29, that pass found 3 issues. An independent `/code-review`
  of the same change found 9, including the structural fix (a check that would have caught the
  0.2.2 drift), and later rounds kept finding real defects.
- **`grill-with-docs` cannot be started by an agent.** Its frontmatter sets
  `disable-model-invocation: true`. Its body is only "Run a `/grilling` session, using the
  `/domain-modeling` skill", and both of those are agent-invocable.

## Decisions

All grilled with the human one question at a time (`grilling`), each with a recommendation.

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| What the pre-PR review is for | (a) independent second reader; (b) author's checklist | (a) | The human is the final gate; the missing piece before it is a reader not anchored on the author's reasoning | Human |
| How the skill names the reviewer | (a) `superpowers:requesting-code-review` everywhere; (b) by role, default per agent; (c) a tool per agent | (b): `/code-review` in Claude Code, `superpowers:requesting-code-review` elsewhere | Naming the role survives tool churn; `/code-review` was measured on real diffs, the superpowers reviewer wasn't yet | Human |
| `code-review-skill` | (a) remove everywhere; (b) keep as optional | (a) | An optional list item still costs attention and had drifted across three install paths | Human |
| Grilling companion | (a) `grilling` + `domain-modeling`; (b) agent asks the human to type `/grill-with-docs`; (c) `brainstorming` only | (a) | Same behaviour minus the switch that blocks the agent; (b) makes the human the trigger; (c) loses decision-by-decision resolution and the ADR record | Human |
| New wording for Copilot without `superpowers` | add guidance; none | None | Baseline: 3/3 agents already tell the human and claim nothing (writing-skills: no failure, no guidance) | Agent, from the eval |
| Form of the new review wording | prohibition ("don't self-review"); recipe ("the review is …") | Recipe | The baseline failure was obedient to the old wording, not a rationalisation; writing-skills says shape problems take a recipe | Agent |

## What was done

- `skills/disciplined-delivery/SKILL.md`: Requires (independent reviewer; `grilling` +
  `domain-modeling`; `requesting-code-review` listed under superpowers), loop step 1, loop step 6,
  Decisions & docs; step 6 now says commit, then run `/code-review <default-branch>...HEAD` (or
  `requesting-code-review` with the merge base and the requirements).
  `description` untouched.
- `docs/adr/0001-…`: the decision record (the repo's first ADR; `docs/adr/` added to the layout in
  README and CLAUDE.md), the index `docs/adr/README.md`, and `tests/test_adr_index.py`.
- README (how-it-works prose, diagram, agent prompt, Claude Code install steps inside the
  `install-check` markers, components table, verify steps, Copilot companions), `install.sh`,
  `CLAUDE.md`, `CONTRIBUTING.md`, the eval case expectation and the pending transcript template.
- `CHANGELOG.md` Unreleased → Changed.

## Verification / evidence

- **Wording A/B** (`evals/transcripts/disciplined-delivery-2026-10-27-wording.md`), fresh Opus 5.5
  subagents, same prompts and same available skills in both arms:
  S1 independent review **0/3 → 3/3**; S2 agent starts grilling **0/3 → 3/3**; S3 regression
  check **3/3 → 2/2**. Baseline S1 runs said outright that they would not use an independent
  reviewer "because the skill doesn't call for them"; one green run volunteered that
  `code-review-skill` "would run inside my own session".
- **Independent review of the branch** (`/code-review`, medium) found 8. Fixed: the review must
  cover `main...HEAD` after committing (requesting-code-review diffs commits, so an uncommitted
  change went unreviewed); the requirements are passed in [corrected in round 3: only to
  `requesting-code-review`; `/code-review` takes none]; Copilot names the skill bare; the
  `domain-modeling` wording (it writes ADRs only for hard-to-reverse decisions); an ADR index and
  guard test (`tests/test_adr_index.py`, each test mutation-checked); this report's status.
  Refuted: "/code-review may run in the author's context" — it ran forked here and, on #29,
  re-raised a claim already refuted in the author's session. Covered: Copilot without
  superpowers falls to the existing "no independent review" disclosure (2/2 S3 runs did).
  GREEN re-run on the revised wording: S1 3/3 (stricter pass), S2 3/3.
- **Rounds 2 and 3** (8 and 10 findings): fixes listed in the change log below and the PR. S1 on
  the final wording (`/code-review <default-branch>...HEAD`): 2/2.
- Local CI, independent review and CI results: see the PR (named SHA).

## Outstanding / next steps

- **Live auto-trigger eval** (`evals/transcripts/disciplined-delivery-pending.md`) is still owed.
  This change leaves the `description` alone, so loading should be unaffected, but that is
  inferred, not run.
- **The scenario runs are self-reported plans**, not observed tool calls in a live session. A
  live S1 run (does the agent actually invoke `/code-review`?) would be stronger evidence.
- **No fallback for a missing `superpowers` outside Claude Code**: every S3 run noted it, all
  handled it well. Revisit only if a run fails.
- `superpowers:requesting-code-review` is the non-Claude default but **has not been measured** on
  a real diff in this repo.
- Next planned PR (E): hooks so the gates are hard to skip, as grilled on 2026-10-27 (see the
  maintainer's plan; decisions 6–12).

## References

- `superpowers:writing-skills` (RED/GREEN/REFACTOR for skills; "Match the Form to the Failure")
- `~/.claude/skills/grill-with-docs/SKILL.md` (`disable-model-invocation: true`)
- `superpowers` 7.0.0 `skills/requesting-code-review/`

## Change log

- 2026-10-27: created.
- 2026-10-27: third review round: `/code-review` takes no requirements and, with no target,
  reviews only unpushed commits, so the skill names the range and drops the requirements claim
  for it; stronger ADR guard; Copilot cloud-agent companions.
- 2026-10-27: first review round's fixes recorded under Verification; second round's fixes
  (transcript de-duplicated, base branch not hard-coded in the skill, stronger ADR guard).
