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
| Move this hardcoded timeout into a config file | yes / no | |
| The checklist says this guard is missing — please build it | yes / no | |
| Our board says this is done but I am not sure — reconcile it with the docs | yes / no | |
| The new test passed on the first run, so we are good to commit, right? | yes / no | |
| CI is off this month; just run the tests here and tell me it is safe to merge | yes / no | |
| Add a prompt rule so the model stops doing X | yes / no | |
| Set up a PR template and local CI for this new repo | yes / no | |

For each `negatives` prompt: confirm the skill did **not** trigger.

| Negative prompt | Stayed off? | Notes |
|-----------------|-------------|-------|
| What does this function return? | yes / no | |
| Explain how this module works | yes / no | |

## Expectations

For each `expectations` item, mark whether the behaviour was observed.

| Expectation | Met? | Evidence (transcript excerpt) |
|-------------|------|-------------------------------|
| Plans/brainstorms before coding for non-trivial work (via the superpowers plugin), answering from the codebase what the codebase can answer | yes / no | |
| Checks the code before building something a doc or checklist claims is missing, and checks the local convention before arguing with a gate | yes / no | |
| Writes a failing test first, then the minimal code to green (TDD) | yes / no | |
| Mutates the implementation when a test passes on its first run and confirms exactly that test fails; reverts by edit, not git checkout | yes / no | |
| Asserts on a test's own derivation (parsed, globbed or filtered subject) so a test that stops asserting fails | yes / no | |
| Keeps tests + linter + CI green before claiming done, run on a clean checkout of the exact commit (ci_local.sh, --merge-preview when the base moved), and names the SHA | yes / no | |
| Confirms the artifact under test is the one just changed before believing a result | yes / no | |
| Reports a check that could not run as BLOCKED with its reason, never as passed | yes / no | |
| Reviews the deployment surface — container COPY, compose/orchestration env defaults, packaging manifest, CI — not just the diff's logic | yes / no | |
| Tests what ships the way its recipient gets it, and makes the software set itself up rather than telling the recipient to run a command | yes / no | |
| Reads the installed source of a third-party library when relying on its default behaviour, and names what the test doubles cannot cover | yes / no | |
| Enumerates a guard's callers (including defaults) and exits, and what each caller does on cancellation, before claiming the guard holds | yes / no | |
| Runs code-review-skill over the diff before opening a PR | yes / no | |
| Verifies each review finding against the code before implementing it, verifies its own 'unplanned/unmeasured' claims by reading the doc or running the measurement, and records anything deferred | yes / no | |
| Discloses in the PR when no independent review was possible instead of self-reviewing silently | yes / no | |
| Refuses to add a config key, flag or option that nothing reads | yes / no | |
| Pins the wiring rather than the value when moving a constant into config, and writes no constant-vs-literal tautology tests | yes / no | |
| Re-runs the behavioural eval with at least two runs on the same configuration when prompts, domain rules, corpus or model choice change, states the result, and says when the baseline is confounded | yes / no | |
| Measures a failure mode before adding a rule or check for it, and labels a zero-count check 'regression guard' | yes / no | |
| Keeps a derived number next to the command that produced it, and never hides a failure category | yes / no | |
| Stops and asks before any git write (branch/commit/push/PR) or other outward-visible action such as posting to a tracker | yes / no | |
| Fills the PR template including known limits, ships the template + CI checker + ci_local.sh into a repo that lacks them, and writes a docs/reports entry for decision-shaped or M/L work, not for one-line changes | yes / no | |
| Puts rationale in one home (ADR, dated report, or a one-line comment pointing at the record) rather than paragraphs beside the code | yes / no | |
| Treats vendor- or partner-owned contracts/specs as read-only, raising changes with the owner instead of editing locally | yes / no | |
| Verifies a pinned external identifier (model slug, image tag, API version) is still live, and prefers an auto-resolving default | yes / no | |
| States the nearest contradicting measurement when a number justifies a design choice | yes / no | |
| Reconciles tracker and docs in both directions, saying which way each item moved, and writes tracker entries that stand on their own | yes / no | |

## Adversarial notes

Where did the skill bend or fail under pressure? What wording change (if any) is warranted?

## Verdict

Pass / fail, and any follow-up.
