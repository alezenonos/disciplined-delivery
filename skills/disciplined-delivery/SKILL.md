---
name: disciplined-delivery
description: Use when implementing a change in a repo that ships work as small, human-reviewed pull requests — especially before committing, branching, pushing, or opening a PR.
---

# Disciplined Delivery

## Overview

Ship work as **small, test-first, individually reviewable increments**, and let the **human** be the gate that commits and merges. Optimise for a reviewer who reads every diff — not for speed of landing code.

**Core principle:** one focused change, proven green on a clean checkout of the exact commit, presented for review — then ask before any git write, or any other action the outside world can see.

This skill does not reinvent planning or testing discipline: **planning and brainstorming run through the `superpowers` plugin** (`brainstorming`, `writing-plans`), and so does **test-driven development** (`test-driven-development`) and final verification (`verification-before-completion`). This skill orchestrates them and owns the review-gate discipline around them.

Every gate here earned its place by catching something real on a project that used this skill for months; `references/gates.md` records what each caught and what it costs, and `references/evidence.md` the rules for measuring, claiming and recording. Read them when a gate below is not self-explanatory. **A gate that stops paying for itself is deleted** — that is why the cost is written down.

## Requires

This skill leans on companion skills and does not reimplement them:

- **`superpowers`** (obra) — declared as a plugin dependency in `plugin.json`, so Claude Code installs it automatically. Provides `brainstorming`, `writing-plans`, `test-driven-development`, `requesting-code-review`, `receiving-code-review`, and `verification-before-completion`, used in the loop below.
- **`grilling`** and **`domain-modeling`** (mattpocock/skills) — relentless design interrogation, one question at a time, with the outcome recorded as ADRs + a glossary (`CONTEXT.md`) as decisions crystallise. Both are agent-invocable: **you start them yourself**. Ship via `skills.sh`, not as a plugin, so they cannot be `plugin.json` dependencies: install once with `npx skills@latest add mattpocock/skills` (select `grilling` and `domain-modeling`).
- **An independent reviewer** — the pre-PR review is done by a reviewer that sees **only the diff and the requirements, never your session**. In Claude Code use the built-in **`/code-review`**; elsewhere use **`superpowers:requesting-code-review`**, which dispatches a fresh reviewer subagent.

## Ships with (copy into the consuming repo)

`assets/` holds the mechanisms the rules below lean on, ready to copy. A rule that only people remember is not enforced; each of these turns a rule into a check:

- **`PULL_REQUEST_TEMPLATE.md`** → `.github/PULL_REQUEST_TEMPLATE.md`. Problem, change, how tested (naming the commit), alternatives, known limits, single-change attestation, review boxes for behaviour-shaping and shipped changes.
- **`check_pr_template.py`** → `.github/scripts/`, with **`pr-template.yml`** → `.github/workflows/`. Fails the PR when a template section is missing, a prose section still holds the guidance comment, or the single-change box is unticked. The rules are read from the template, so the repo changes what a PR must say by editing the template alone.
- **`ci_local.sh`** → wrap it as `scripts/ci_local.sh` with the exact checks CI runs. It runs them on a **temporary clean checkout of the commit**, never the working tree, and `--merge-preview` tests the commit merged with the base, as the host's CI tests a PR. It prints the SHA it tested.

## When to use

- Implementing any feature, bugfix, refactor, or docs change.
- Before `git commit`, `git push`, creating a branch, or opening a PR.

Not for: throwaway spikes, or repos with no review process (still verify before claiming done).

**Companion:** starting a brand-new agentic/RAG LLM app? Bootstrap the structure once with the sibling `scaffold-agentic-app` skill (in this plugin, invoked as `/disciplined-delivery:scaffold-agentic-app`), then return here and build every feature as a small, reviewed increment.

## The loop (per change)

1. **Think first — plan and brainstorm via `superpowers`.** Ambiguous goal or load-bearing decision? Before coding, brainstorm and plan using the **superpowers** plugin (**REQUIRED:** `superpowers:brainstorming` for non-trivial design; `superpowers:writing-plans` for multi-step work), and **start `grilling` with `domain-modeling` yourself** to stress-test any load-bearing decision before you commit to it: questions one at a time, each with a recommended answer, and **anything answerable from the codebase is answered there rather than asked**. Grill tasks together when they share a surface. Simplest thing that works — no speculative abstraction, no drive-by refactors.
2. **Establish the ground truth in code.** Before building something because a doc, checklist, ticket, or ADR says it is missing — **grep the code**. Documents lie: an unticked acceptance checkbox is not evidence that the work is undone, and a task board is not evidence that it is. Confirm the gap exists, then close it. When a gate objects, **look at how the code already meeting it does so, first** — the convention that resolves the argument is usually two files away.
3. **TDD, red-first — via `superpowers`.** Drive the change test-first using the **superpowers** plugin's TDD discipline (**REQUIRED:** `superpowers:test-driven-development`). Watch the test fail *for the right reason*, then write the minimal code to green. **A test that passes the moment you write it has proven nothing yet: mutate the implementation and confirm that exactly that test fails.** Revert the mutation with an edit, never with `git checkout` (it has destroyed uncommitted work). Before trusting a survived mutation, **confirm the test is still asserting on something**: where a test derives its subject (parses a file, globs paths, filters a list), assert on the derivation too — `assert len(found) >= 5, "extraction looks broken"`.
4. **Verify** (**REQUIRED:** `superpowers:verification-before-completion`). Full test suite + linter green, **on a clean checkout of the exact commit** (`scripts/ci_local.sh`; `--merge-preview` when the base has moved), and the **CI pipeline green** on the pushed branch — a working-tree green is not "done", and local-only green is not "done". **Confirm the artifact under test is the one you just changed** (bust the cache, print the version, assert on something only the new code could do): a stale page, a buffering transport or yesterday's report all pass or fail for reasons that are not yours. The lines you touched are covered. **Claim only what you actually ran, and name the SHA it ran on**; "not checked" is never "passed" — a check that could not run is BLOCKED, with its reason.
5. **Review the whole surface** — see the section below. A green suite proves the logic; it does not prove the change works where it ships, nor that a guard reaches every path.
6. **Stop and ask.** Leave the result as uncommitted working-tree changes, summarise, and **ask before any git write** (branch / commit / push / PR) **or any other outward-visible action** — posting to a task tracker, commenting on an issue, sending a message, deploying. Reading, editing, and running tests need no permission; anything the outside world sees does. When the human approves proceeding to a PR, **first get an independent review**: a reviewer that sees only the diff and the requirements, never your session (`/code-review` in Claude Code; `superpowers:requesting-code-review` elsewhere). Your own pass over your own diff is not the review. Resolve every blocking/important finding before opening the PR.

## Review the whole surface

A passing suite proves the logic. It does not prove the change works in the places it actually runs. Before opening a PR, walk these explicitly:

- **Deployment paths.** Does the change work in *every* way this project ships? Derive the list from how this repo actually ships, then check each by name. For a containerised Python service that is: container build files (is a new file `COPY`ed?), compose/orchestration env blocks (does an injected default silently override the config knob you just added?), the packaging manifest (is the new module/data file included?), CI workflows. For a library it is the published artefact and its extras; for a frontend, the bundle and its runtime config. **A value that lives in more than one place — env, orchestration, config file, code default — rots out of sync silently.** The same applies to a *rule* stated in more than one document.
- **Test what ships, the way its recipient gets it.** Exercise the real artefact (the built image, the installed package, the other team's checkout at the exact commit), not a description of it: a test that reads source text, or a fake standing in for a dependency, cannot fail when the dependency is missing. **A handoff needs no command from its recipient** — the software sets itself up, or stops at once with a message that needs no terminal; a setup note in the PR is a courtesy, never the fix.
- **Third-party defaults you rely on.** When behaviour depends on a library's default, **read the installed source** rather than trusting memory or docs. Vendored defaults can silently override or multiply your intent, and test fakes usually replace the library entirely — so the suite cannot see it.
- **A guard is only as good as the paths it reaches.** A bound, a stop flag, a cap, a seeded scope is written once and then *claimed* everywhere; the mechanism is usually right and the claim is false for one path. Before claiming a guard holds: `grep` its callers and what each passes (a default of `None` is a path, not an absence); enumerate its *exits*, not just the happy one; ask what each caller does on cancellation, not only on the condition you designed for. Name the zero point of any bound, parametrise a derived bound past its shipped value, and bound the artefact the operator actually sees, after all encoding.
- **What the tests structurally cannot cover.** Name it out loud. If every test double bypasses the real client, the real client's behaviour is unverified no matter the coverage number.
- **Escalate when** the change adds a config knob or a new shipped file, alters client/SDK construction, or changes precedence between env and config. Those are where "green but broken where it ships" lives.
- **If the reviewer cannot run** (unavailable, rate limited, budget exhausted): say so plainly, state in the PR body that the diff had **no independent review**, and walk this checklist explicitly yourself. Never let a self-review pass silently as a review.

## Receiving review findings

Reviews are input to verify, not orders to execute, and not noise to wave away.

- **Verify each finding against the code before acting** (**REQUIRED:** `superpowers:receiving-code-review`). Confirm it, then fix the root cause — or explain, with evidence, why it does not hold. Reviewer findings are usually right; knowing that comes from checking, not deference.
- **Verify your own claims the same way.** "Unplanned", "unmeasured", "all defensive", "would pollute retrieval" — each was asserted and each was wrong on inspection, because nobody read the document that planned it or ran the measurement. Read it, or run it, before asserting it.
- **Fix the cause, not the symptom.** If a finding reveals that your justification was wrong, correct the justification too, not just the line.
- **Record what you deferred and why.** A finding you consciously decline is a decision; an undocumented one is a leak.
- **Cite the data that contradicts you.** When a number justifies a design choice, state the nearest contradicting observation and why it does not change the call. Quoting only the supporting measurement is how a reasonable-looking default ships wrong.
- **Repeated findings on your pushes mean fix the root cause**, not stop. Independent review rounds found 11, then 9, then 6 issues on one check — each round's fix was written test-first and mutation-checked.

## Branch & PR conventions

- One branch = one focused change. Name it `feat/…`, `fix/…`, `chore/…`, `docs/…`, `test/…`; target the default branch.
- **Avoid stacked PRs.** If a series is unavoidable, keep each off the default branch and merge **bottom-up**, letting the host retarget the next before merging it.
- **The PR template is mandatory, and a check enforces it.** Use the consuming repo's `.github/PULL_REQUEST_TEMPLATE.md` (ship `assets/PULL_REQUEST_TEMPLATE.md` if it has none) and its CI check (`assets/check_pr_template.py` + `assets/pr-template.yml`) — fill **every** section honestly. Blank sections, placeholder text, bundled changes, or no evidence of human review get the PR closed without review.
- **PR bodies carry the known limits**, not only the wins — a confounded baseline, a gap left open, a check that could not run, a rejected alternative and why. If a limit is worth knowing at review time it is worth writing.
- **A gate must render in an enforcing surface.** A rule that lives only in prose is the inert-config failure applied to process. Put it in the template as a checkbox (with wording that covers every case it applies to — "prompt *or corpus* change", not "prompt change"), in a CI check, or in a script that refuses; and keep the check's cost in proportion (measure what CI minutes buy; never skip CI by path filter — a renamed file is judged by its new path).
- **Skills are code, not prose.** Changing a skill's behavior-shaping wording requires adversarial testing and eval evidence (use `superpowers:writing-skills`), per the template's Rigor section — not just a happy-path check.

## Commit hygiene

- Conventional subject (`type(scope): summary`); the body explains **the decision**, not the diff.
- **Never put backticks or `$(…)` inside `git commit -m "…"` or `gh … --body "…"`** — the shell runs them as command substitution, mangling the message and possibly your environment. Use a quoted heredoc (`git commit -F - <<'EOF' … EOF`) or `--body-file`.
- End with any required trailer (e.g. `Co-Authored-By:`).

## Engineering standards

Every repo this skill ships into is held to these — they are part of "done", not optional polish:

- **Code quality & style.** Code follows the language's accepted style guide — for Python, **PEP-8** plus the **Google Python Style Guide** (naming, import order, docstring sections, line length). This is **enforced by the linter in CI**, not by reviewer taste: the linter config (e.g. `ruff` in `pyproject.toml`) *encodes* the standard so violations fail the build, and silencing the linter to get green is a red flag, not a fix. Beyond the rules, write the simplest correct code — small functions, clear names, no speculative abstraction (see the working principles in `CLAUDE.md`).
- **A CI pipeline exists and gates merges.** There is a `.github/workflows/` (or equivalent) pipeline that runs the test suite, linter, and any project-specific validation (e.g. manifest/schema checks) on every push and PR. A change is not done until CI is **green** on the branch; a red or *absent* pipeline is a blocker, not a footnote. New repos without CI: add it as part of the first change. **Local CI mirrors it exactly** (`scripts/ci_local.sh` wraps the same commands) so the two cannot drift.
- **Tests must be able to fail.** A test that compares a constant to a literal (`assert TIMEOUT > 74`) pins nothing and catches nothing. Test **behaviour**, and when you move a value into config, **pin the wiring, not the value** — assert the runtime constant comes *from* the config, so re-hardcoding fails while tuning stays a one-file change. A test whose harness cannot exercise the behaviour it is named for (a transport that buffers, a fake that bypasses the seam) is deleted, not kept.
- **Configuration is loaded fail-fast, and nothing is dead.** A config loader validates on load — missing key, wrong type, out-of-range value, and **unknown keys** — so a typo cannot read as "configured" while the real default silently stays in force. Never add a config key, flag, or option that nothing reads: a dead knob is worse than no knob, because it advertises control that does not exist. **Exception — fail closed on privacy:** anything that governs what *leaves* the process (telemetry capture, transcript export) degrades an unrecognised value to the safest setting, so a typo costs observability and never exports a conversation.
- **Diagnostics degrade, never abort.** A broken golden file, an unreachable tracing backend, a coverage upload that cannot connect, a failing judge costs that *signal*, never the run (`continue-on-error` on the upload step; a guarded loader that logs and continues). A diagnostic must not be able to fail a turn, a build, or a paid run.
- **Every check reports its state honestly.** PASS, FAIL, BLOCKED or NOT APPLICABLE, each with its reason; a check that could not run is never shown as passed; a partial result is shown as partial. Every failure cause is printed, including `other`, and the counts add up to the total.
- **Whatever runs, releases or deploys the product is a reviewed script in the repository**, never a scratchpad or a remembered sequence. A release records its artefact and the commit, refuses a commit whose required evidence (tests, behavioural runs) is missing unless told why, and every production change is logged with how to undo it. A healthy `/healthz` does not prove an answer: after a change, someone uses the product and writes down what happened.
- **Pinned external identifiers rot.** Model slugs, image tags, API versions, dataset ids: verify a pin is still live against the source of truth, and prefer an auto-resolving default where one exists. When you must pin, note where it is verified.
- **Vendor- or partner-owned inputs are read-only.** Contracts, schemas, or specs another team owns are consumed as-is. If one needs a change, raise it with the owner — never edit it locally, and never add local metadata to it. Where their source is readable, **a check compares your specs against it** rather than a person noticing a drift by chance.
- **A professionally written README.** Clear and current: what the project is, how to install/run it, how to develop and test it (the exact commands CI runs), and the project layout. No stale instructions, no placeholder text. Update it in the same change that changes behavior. **Counts embedded in prose rot** — "the 36-prompt battery" goes stale the moment the thing changes; drop the number or assert it in a test.
- **Documentation, including docstrings.** Public modules, classes, and functions carry docstrings that say what they do and why — not restatements of the signature. A module opens by naming its purpose, its invariants, and the records that shaped it. Keep docs in sync with the code in the same commit; out-of-date docs are a bug.
- **Project memory (`CLAUDE.md`).** Maintain a `CLAUDE.md` at the repo root holding agent instructions and project conventions (how to build/test, where things live, working principles, the repo's norms with the report that earned each). Keep it current as conventions change.

## Behaviour-shaping changes (LLM apps)

When the change alters what a model sees or does — prompts, system-prompt fragments, domain rules, **the corpus**, tool specs, model choice, or the code that composes the answer — the unit test suite is not the gate:

- **Re-run the behavioural eval** (golden set, battery, or scored suite) and **state the result in the PR**. Make it a checkbox in the PR template so it cannot be forgotten, worded to cover every input that changes behaviour. **Two runs, or no claim:** a single run cannot distinguish a regression from sampling variance, so any behavioural claim needs at least two runs on the same configuration. Compare against a baseline, and **say when the baseline is confounded** (an old run on a base that has moved) rather than claiming a win.
- **Choose the subset by whether the change narrows or broadens behaviour.** A caveat or prohibition (narrowing): the prompts already on that path suffice. A fallback or "also do X when…" (broadening) can fire anywhere, so include the classes a targeted subset would exclude.
- **The release refuses what was not measured.** The release script checks that the runs exist for the exact prompt, corpus and answer-making code it ships, and releases an unmeasured commit only with a written reason.
- **Keep the prompt in configuration, not in source**, so a domain expert can review and revise it without reading code — and compose it fail-fast, so a missing fragment breaks the boot rather than silently shipping a prompt with a hole in it. If a change to what the product *says* requires a code change, the seam is in the wrong place.
- **Separate the lanes:** domain-owned content (terminology, interpretation, conduct) in files the domain expert edits; engineering-owned orchestration and safety rules in code. Say which lane a change belongs to.
- **Never claim an answer is correct.** Reports separate what is machine-verified (trajectory, tool choice, hygiene) from what needs the domain owner's approval (faithfulness), and say so. Do not author golden expectations yourself — those are the domain owner's words, and writing them scores you against your own opinion.

## Measurement & rules

- **Measure before you add a rule or a check.** Never ship a prompt rule or an eval check for a failure mode you have not counted in the run archives. A check for something that occurs zero times is legitimate, but it says **"regression guard"** in its comment and its report — never presented as a fix.
- **Report, never exclude.** A number that flatters by hiding a category is worse than an ugly number. Every failure cause is printed; a count that does not add up to the total is a bug.
- **Measure the question actually being asked.** Before reporting a measurement, state what it would take for the conclusion to be false, and check that the measurement could detect it.
- **A derived number carries the command that produced it**, with its filter criteria, next to the figure in the document. A number is quotable only next to the run that produced it; restating a figure from a description of the evidence is where the errors are.
- **Evidence artefacts are immutable.** Never overwrite a committed run or report; re-render to a new name.

## Decisions & docs

- Grill the load-bearing choices before building (start **`grilling`** with **`domain-modeling`**, which records them as ADRs + a glossary as you go); capture **deferred/blocked** decisions as short ADRs (status *Proposed*, a recommendation as a *lean* not a verdict — the human decides).
- **Rationale has one home, and the code carries a pointer to it.** A *decision* lives in an ADR; a *measurement* in a dated report; what is *locally non-obvious* (an invariant, a trap) in the comment beside the code — one line stating the invariant and pointing at the record (an ADR id or a `docs/…` path, never a bare PR number). A decision index maps records to the code that carries them; a guard test fails when code cites a record that does not exist. Migrate on touch, not in a sweep.
- Living docs carry a **Created / Last-edited** header with a per-edit change-log. Reports are self-contained and claim only what is machine-verified; flag the rest for human review. **Corrections stay visible:** a wrong conclusion is marked `[corrected]` in place with the reasoning error named, never silently rewritten.
- **Dated reports are immutable snapshots.** When a later finding invalidates a planning doc, patch the **planning** doc (dated) and leave the snapshot as the record of what was known when. Do not rewrite history to look consistent.
- **Task reports, scaled to the task.** **Sizing:** XS/S = one file, no interface/contract/behaviour change; **M/L = anything else** — several files, a new module or config surface, a changed public interface or contract, or a call someone could reasonably disagree with. M/L and decision-shaped work produces a report under `docs/reports/` (named `YYYY-MM-DD-<slug>.md`, from the repo's `docs/reports/_TEMPLATE.md`): the task, the **decision-making process** (options, choices, who decided), what was done, evidence, and **outstanding items** — enough that a collaborator can pick the work up cold. For XS/S changes, a well-filled PR description is the report; do not manufacture ceremony for a one-line change. Be honest about what is not done. **Write the report even when the answer is "no"** — a measured negative is a deliverable, and an idea tested and declined is worth more written down than deleted.
- **Keep a living "how we work" description, not a rulebook.** Each gate lists what it caught and what it costs; a gate that is not paying for itself is deleted. The repo's `CLAUDE.md` names each norm with the report that earned it.
- **Reconcile the tracker and the docs in both directions.** The board holds items the docs missed, and vice versa. When syncing, expect to learn in both directions and say which way each item moved. **Anything written to a shared tracker stands on its own** for someone who was not in the conversation: no run stamps, no internal shorthand, no file paths in place of saying what the problem is; quote people verbatim, with the date. A tracker entry may *record* that a question is owed; it must never *ask* it on the human's behalf.

## Red flags — STOP

- About to commit / push / open a PR — or post, comment, message, deploy — without asking.
- Bundling unrelated changes into one PR.
- "It's too small to test / template / ask."
- Claiming "done", "passing", or "fixed" without having run it — on the working tree instead of a clean checkout of the commit, or while CI is red or missing.
- Trusting a test that passed on its first run without mutating the code it covers — or trusting a survived mutation without checking the test still asserts anything.
- Believing a result before confirming the artifact under test is the one you changed.
- Claiming a guard holds without enumerating its callers and its exits.
- Building something because a doc or ticket says it is missing, without checking the code.
- Reviewing only the diff's logic — never asking whether it works where it ships, or trusting a library's default from memory instead of reading its installed source.
- Telling a recipient to run a command after pulling, instead of making the software set itself up.
- Self-reviewing silently because the reviewer was unavailable.
- Implementing a review finding without verifying it — or dismissing one without evidence.
- Quoting the measurement that supports the choice while a contradicting one sits in the same table.
- Making a behavioural claim from one run, or adding a rule for a failure you have not counted.
- Showing a check that could not run as passed, or a count that hides a category.
- Adding a config key, flag, or option that nothing reads.
- Shipping code with no docstrings, or leaving the README stale after a behavior change.
- Silencing the linter (blanket `# noqa`, disabling rules) to go green instead of fixing the code or the style standard.
- Backticks inside a `-m`/`--body` string.

Each of these means: stop, scope down, verify, and hand the gate back to the human.
