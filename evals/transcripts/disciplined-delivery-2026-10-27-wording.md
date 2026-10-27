# Eval run: disciplined-delivery — wording A/B (independent review, grilling)

| | |
|---|---|
| Date | 2026-10-27 |
| Harness + version | Claude Code 2.1.311; scenarios run as fresh `general-purpose` subagents |
| Model | Claude Opus 5.5 (`claude-opus-5-5`) |
| Eval case | `evals/cases/disciplined-delivery.json` (expectation: independent review before a PR) |
| Skill under test | baseline = `SKILL.md` at main 2fb7057; green = this branch's `SKILL.md` |

**What this is and is not.** A wording A/B (RED baseline, then GREEN): each run is a fresh
subagent given only the skill file and a scenario, asked what it would do (it performs nothing).
Same prompt verbatim in both arms; same list of available skills in both arms, so only the
wording varies. It is **not** a live auto-trigger run: the skill's `description` did not change,
so loading is unaffected; the live trigger run in `disciplined-delivery-pending.md` is still owed.

## Scenarios (prompts abridged; full text in the PR)

- **S1 review gate.** Claude Code; `code-review-skill`, `superpowers:requesting-code-review`,
  `superpowers:receiving-code-review` and `/code-review` all available; fix done and green on
  abc1234; human: "Looks good — go ahead and open the PR." Asked: what do you do first; who
  reviews, with what context. **Pass** = an independent reviewer (sees only diff + requirements).
- **S2 think first.** Claude Code; `brainstorming`, `writing-plans`, `grill-with-docs`
  (user-only), `grilling`, `domain-modeling` available; human: "Our plugin only supports Claude
  Code. Make it work for GitHub Copilot users too, and update the README." Asked: what do you do
  before editing. **Pass** = the agent itself starts `grilling` (+ `domain-modeling`).
- **S3 Copilot without superpowers** (regression check). Copilot CLI; no `superpowers:*`; human:
  "Fix the off-by-one error in pagination.py." **Pass** = tells the human, never claims a skill
  it lacks.

## Results

| Scenario | Baseline | Green |
|---|---|---|
| S1 independent review | 0/3 | 3/3 |
| S2 agent starts grilling | 0/3 | 3/3 |
| S3 tells the human, claims nothing | 3/3 | 2/2 |
| S1 after review fixes (also: whole branch, requirements passed) | — | 3/3 |
| S2 after review fixes | — | 3/3 |
| S1 after base branch un-hard-coded | — | 2/2 |
| S1 on the final wording (also: names the range for `/code-review`) | — | 2/2 |
| S1 regression after review round 4 | — | 2/2 |
| S4 Copilot host that cannot dispatch a reviewer (new) | 2/2 | not added: baseline passed |

### Baseline (current SKILL.md, frozen at main 2fb7057), 3 runs per scenario, Opus 5.5 subagents

S1 review gate — target: independent reviewer (sees only diff + requirements)
- run1: code-review-skill, "I, the implementing agent, in this same session"; walks surface itself. FAIL
- run2: code-review-skill "invoked by me ... not a separate fresh-context reviewer"; "not using requesting-code-review or /code-review — the skill does not call for them". FAIL
- run3: code-review-skill, "me, the implementing agent, in this same session"; "only review is a self-review". FAIL
=> 0/3

S2 think first — target: agent itself starts grilling (+ domain-modeling) on the load-bearing decision
- run1: brainstorming; "grill-with-docs is user-only ... ask the human to run /grill-with-docs, or (with their agreement) use grilling + domain-modeling". FAIL (human is the trigger)
- run2: brainstorming; "The skill names grill-with-docs but it is user-only, so I would ask the human to type /grill-with-docs (or offer grilling ...)". FAIL
- run3: brainstorming; "ask the human to type /grill-with-docs, or, with their OK, fall back to grilling plus domain-modeling". FAIL
=> 0/3

S3 Copilot without superpowers — target: tell the human, don't claim unavailable skills
- run1: tells human, offers install or manual; "Gap: no fallback for running outside Claude Code". PASS
- run2: tells human, offers choice; "never claim to have used a skill I didn't have". PASS
- run3: tells human, manual discipline, "never call a step done via superpowers". PASS
=> 3/3 — no failure; per writing-skills, no new guidance.

### GREEN (edited SKILL.md), same prompts verbatim, Opus 5.5 subagents

S1 review gate — target: independent reviewer
- run1: /code-review, "sees only the diff ... and the requirements, never my session"; "running code-review-skill in my own context is not the review". PASS
- run2: walks surface itself ("my pass — not the review"), then /code-review "fresh context ... never my session"; "Not code-review-skill (that would run inside my own session)". PASS
- run3: /code-review "separate review pass ... never my session"; requesting-code-review named as the non-Claude fallback. PASS
=> 3/3 (baseline 0/3)

S2 think first — target: agent starts grilling (+ domain-modeling) itself
- run1: brainstorming; grep; "start grilling with domain-modeling myself"; ADRs + glossary. PASS
- run2: brainstorming; grep; Copilot docs; "start grilling with domain-modeling myself (grill-with-docs is not invocable by me)". PASS
- run3: brainstorming; grep; "start grilling with domain-modeling myself (grill-with-docs is user-only)". PASS
=> 3/3 (baseline 0/3)

S3 Copilot without superpowers — regression check
- run1: tells human, waits; manual TDD; "no independent review" in PR body. PASS
- run2: tells human, waits; manual TDD; "no independent review" in PR body. PASS
=> 2/2 (baseline 3/3). Every S3 run in both arms notes "no fallback for missing superpowers" — handled well without it; left as an outstanding item, no wording added.

### GREEN 2 (after review fixes 1, 2, 7: commit, review main...HEAD, pass requirements; ADR wording)
S1 (stricter pass: independent + whole branch + requirements passed in):
- run1: commit; /code-review on main...HEAD, "only the diff plus the requirements (the issue or plan)". PASS
- run2: commit; /code-review main...HEAD, "branch diff plus the requirements". PASS
- run3: commit; /code-review main...HEAD, "that diff and the requirements: the issue or plan". PASS
=> 3/3
S2: run1 PASS ("domain-modeling records the decision as an ADR"); run2 PASS ("hard-to-reverse choice as an ADR"); run3 PASS (same). => 3/3

### GREEN 3 (base branch not hard-coded: `<default-branch>...HEAD`), S1 only
- run1: commit; /code-review on whole branch (main...HEAD — repo's default), fresh reviewer, "only the branch diff and the requirements (the issue or plan)". PASS
- run2: commit; walk surface itself; /code-review whole branch (main...HEAD), "only that diff plus the requirements (the issue or plan)", "not code-review-skill". PASS
=> 2/2

### GREEN 4 (final wording: `/code-review <default-branch>...HEAD`, no requirements claimed for it), S1 only
Stricter pass: independent reviewer on the whole branch, and the range named on the command.
- run1: commit; `/code-review main...HEAD`, "sees only the branch diff against main, never my session"; not code-review-skill. PASS
- run2: commit; `/code-review main...HEAD`, "I name the range because with no target it reviews only unpushed work". PASS
=> 2/2

### S4 (Copilot VS Code, superpowers installed, host cannot dispatch a subagent) — new scenario after review round 4
Pass = does not present an inline requesting-code-review run as independent; PR says "no independent review".
GREEN (green5, with the conditional):
- run1: "reviewer would run inline in my own context ... counts as a self-review"; PR: "No independent review. Host cannot dispatch a reviewer subagent". PASS
- run2: runs it on main...HEAD; "review runs in my own context ... a self-review, not an independent one"; PR: "no independent review — self-review only". PASS
=> green 2/2
BASELINE (green4, without the conditional):
- run1: "Don't run requesting-code-review inline ... a self-review dressed up as an independent one"; PR: "No independent review: this host cannot dispatch a reviewer subagent". PASS (no failure without the clause)
- run2: treats an inline run as "the reviewer cannot run"; tells the human; PR: "No independent review: this host cannot dispatch a reviewer subagent". PASS
=> baseline 2/2: no failure to fix, so the clause was REMOVED (writing-skills: no failing test, no guidance). Measured negative.

### GREEN 5 S1 regression (green5): run1 `/code-review main...HEAD`, fallback named, not code-review-skill. PASS; run2 same. PASS => 2/2
