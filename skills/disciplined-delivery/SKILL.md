---
name: disciplined-delivery
description: Use when implementing a change in a repo that ships work as small, human-reviewed pull requests — especially before committing, branching, pushing, or opening a PR.
---

# Disciplined Delivery

## Overview

Ship work as **small, test-first, individually reviewable increments**, and let the **human** be the gate that commits and merges. Optimise for a reviewer who reads every diff — not for speed of landing code.

**Core principle:** one focused change, proven green, presented for review — then ask before any git write, or any other action the outside world can see.

This skill does not reinvent planning or testing discipline: **planning and brainstorming run through the `superpowers` plugin** (`brainstorming`, `writing-plans`), and so does **test-driven development** (`test-driven-development`) and final verification (`verification-before-completion`). This skill orchestrates them and owns the review-gate discipline around them.

## Requires

This skill leans on companion skills and does not reimplement them:

- **`superpowers`** (obra) — declared as a plugin dependency in `plugin.json`, so Claude Code installs it automatically. Provides `brainstorming`, `writing-plans`, `test-driven-development`, `receiving-code-review`, and `verification-before-completion`, used in the loop below.
- **`grill-with-docs`** (mattpocock/skills) — relentless design interrogation that stress-tests a plan against your domain model and captures the outcome as ADRs + a glossary (`CONTEXT.md`) as decisions crystallise. Ships via `skills.sh`, not as a plugin, so it cannot be a `plugin.json` dependency: install once with `npx skills@latest add mattpocock/skills` (select `grill-with-docs`).
- **`code-review-skill`** (awesome-skills) — a structured, severity-labelled review (blocking / important / nit / suggestion) across many languages and frameworks. Run before opening a PR. Distributed as a bare skill, not a plugin, so install by cloning into your skills dir: `git clone https://github.com/awesome-skills/code-review-skill.git ~/.claude/skills/code-review-skill`.

## When to use

- Implementing any feature, bugfix, refactor, or docs change.
- Before `git commit`, `git push`, creating a branch, or opening a PR.

Not for: throwaway spikes, or repos with no review process (still verify before claiming done).

**Companion:** starting a brand-new agentic/RAG LLM app? Bootstrap the structure once with the sibling `scaffold-agentic-app` skill (in this plugin, invoked as `/disciplined-delivery:scaffold-agentic-app`), then return here and build every feature as a small, reviewed increment.

## The loop (per change)

1. **Think first — plan and brainstorm via `superpowers`.** Ambiguous goal or load-bearing decision? Before coding, brainstorm and plan using the **superpowers** plugin (**REQUIRED:** `superpowers:brainstorming` for non-trivial design; `superpowers:writing-plans` for multi-step work), and use **grill-with-docs** to stress-test any load-bearing decision before you commit to it. Simplest thing that works — no speculative abstraction, no drive-by refactors.
2. **Establish the ground truth in code.** Before building something because a doc, checklist, ticket, or ADR says it is missing — **grep the code**. Documents lie: an unticked acceptance checkbox is not evidence that the work is undone, and a task board is not evidence that it is. Confirm the gap exists, then close it.
3. **TDD, red-first — via `superpowers`.** Drive the change test-first using the **superpowers** plugin's TDD discipline (**REQUIRED:** `superpowers:test-driven-development`). Watch the test fail for the right reason, then write the minimal code to green.
4. **Verify** (**REQUIRED:** superpowers:verification-before-completion). Full test suite + linter green **locally**, and the **CI pipeline green** on the pushed branch — local-only green is not "done". The lines you touched are covered. Claim only what you actually ran.
5. **Review the whole surface** — see the section below. A green suite proves the logic; it does not prove the change works where it ships.
6. **Stop and ask.** Leave the result as uncommitted working-tree changes, summarise, and **ask before any git write** (branch / commit / push / PR) **or any other outward-visible action** — posting to a task tracker, commenting on an issue, sending a message, deploying. Reading, editing, and running tests need no permission; anything the outside world sees does. When the human approves proceeding to a PR, **first run `code-review-skill` over the diff** and resolve every blocking/important finding before opening it.

## Review the whole surface

A passing suite proves the logic. It does not prove the change works in the places it actually runs. Before opening a PR, walk these explicitly:

- **Deployment paths.** Does the change work in *every* way this project ships? Derive the list from how this repo actually ships, then check each by name. For a containerised Python service that is: container build files (is a new file `COPY`ed?), compose/orchestration env blocks (does an injected default silently override the config knob you just added?), the packaging manifest (is the new module/data file included?), CI workflows. For a library it is the published artefact and its extras; for a frontend, the bundle and its runtime config. **A value that lives in more than one place — env, orchestration, config file, code default — rots out of sync silently.**
- **Third-party defaults you rely on.** When behaviour depends on a library's default, **read the installed source** rather than trusting memory or docs. Vendored defaults can silently override or multiply your intent, and test fakes usually replace the library entirely — so the suite cannot see it.
- **What the tests structurally cannot cover.** Name it out loud. If every test double bypasses the real client, the real client's behaviour is unverified no matter the coverage number.
- **Escalate when** the change adds a config knob or a new shipped file, alters client/SDK construction, or changes precedence between env and config. Those are where "green but broken where it ships" lives.
- **If the reviewer cannot run** (unavailable, rate limited, budget exhausted): say so plainly, state in the PR body that the diff had **no independent review**, and walk this checklist explicitly yourself. Never let a self-review pass silently as a review.

## Receiving review findings

Reviews are input to verify, not orders to execute, and not noise to wave away.

- **Verify each finding against the code before acting** (**REQUIRED:** `superpowers:receiving-code-review`). Confirm it, then fix the root cause — or explain, with evidence, why it does not hold.
- **Fix the cause, not the symptom.** If a finding reveals that your justification was wrong, correct the justification too, not just the line.
- **Record what you deferred and why.** A finding you consciously decline is a decision; an undocumented one is a leak.
- **Cite the data that contradicts you.** When a number justifies a design choice, state the nearest contradicting observation and why it does not change the call. Quoting only the supporting measurement is how a reasonable-looking default ships wrong.

## Branch & PR conventions

- One branch = one focused change. Name it `feat/…`, `fix/…`, `chore/…`, `docs/…`, `test/…`; target the default branch.
- **Avoid stacked PRs.** If a series is unavoidable, keep each off the default branch and merge **bottom-up**, letting the host retarget the next before merging it.
- **The PR template is mandatory.** Use the consuming repo's `.github/PULL_REQUEST_TEMPLATE.md` (this repo ships one, adapted from obra/superpowers) — it is self-documenting; fill **every** section honestly. Blank sections, placeholder text, bundled changes, or no evidence of human review get the PR closed without review.
- **Skills are code, not prose.** Changing a skill's behavior-shaping wording requires adversarial testing and eval evidence (use `superpowers:writing-skills`), per the template's Rigor section — not just a happy-path check.

## Commit hygiene

- Conventional subject (`type(scope): summary`); body explains *why*.
- **Never put backticks or `$(…)` inside `git commit -m "…"` or `gh … --body "…"`** — the shell runs them as command substitution, mangling the message and possibly your environment. Use a quoted heredoc (`git commit -F - <<'EOF' … EOF`) or `--body-file`.
- End with any required trailer (e.g. `Co-Authored-By:`).

## Engineering standards

Every repo this skill ships into is held to these — they are part of "done", not optional polish:

- **Code quality & style.** Code follows the language's accepted style guide — for Python, **PEP-8** plus the **Google Python Style Guide** (naming, import order, docstring sections, line length). This is **enforced by the linter in CI**, not by reviewer taste: the linter config (e.g. `ruff` in `pyproject.toml`) *encodes* the standard so violations fail the build, and silencing the linter to get green is a red flag, not a fix. Beyond the rules, write the simplest correct code — small functions, clear names, no speculative abstraction (see the working principles in `CLAUDE.md`).
- **A CI pipeline exists and gates merges.** There is a `.github/workflows/` (or equivalent) pipeline that runs the test suite, linter, and any project-specific validation (e.g. manifest/schema checks) on every push and PR. A change is not done until CI is **green** on the branch; a red or *absent* pipeline is a blocker, not a footnote. New repos without CI: add it as part of the first change.
- **Tests must be able to fail.** A test that compares a constant to a literal (`assert TIMEOUT > 74`) pins nothing and catches nothing. Test **behaviour**, and when you move a value into config, **pin the wiring, not the value** — assert the runtime constant comes *from* the config, so re-hardcoding fails while tuning stays a one-file change.
- **Configuration is loaded fail-fast, and nothing is dead.** A config loader validates on load — missing key, wrong type, out-of-range value, and **unknown keys** — so a typo cannot read as "configured" while the real default silently stays in force. Never add a config key, flag, or option that nothing reads: a dead knob is worse than no knob, because it advertises control that does not exist.
- **Pinned external identifiers rot.** Model slugs, image tags, API versions, dataset ids: verify a pin is still live against the source of truth, and prefer an auto-resolving default where one exists. When you must pin, note where it is verified.
- **Vendor- or partner-owned inputs are read-only.** Contracts, schemas, or specs another team owns are consumed as-is. If one needs a change, raise it with the owner — never edit it locally, and never add local metadata to it.
- **A professionally written README.** Clear and current: what the project is, how to install/run it, how to develop and test it (the exact commands CI runs), and the project layout. No stale instructions, no placeholder text. Update it in the same change that changes behavior. **Counts embedded in prose rot** — "the 36-prompt battery" goes stale the moment the thing changes; drop the number or assert it in a test.
- **Documentation, including docstrings.** Public modules, classes, and functions carry docstrings that say what they do and why — not restatements of the signature. Non-obvious decisions get a comment or an ADR. Keep docs in sync with the code in the same commit; out-of-date docs are a bug.
- **Project memory (`CLAUDE.md`).** Maintain a `CLAUDE.md` at the repo root holding agent instructions and project conventions (how to build/test, where things live, working principles). Keep it current as conventions change.

## Behaviour-shaping changes (LLM apps)

When the change alters what a model sees or does — prompts, system-prompt fragments, domain rules, tool specs, model choice — the unit test suite is not the gate:

- **Re-run the behavioural eval** (golden set, battery, or scored suite) and **state the result in the PR**. Make it a checkbox in the PR template so it cannot be forgotten.
- **Keep the prompt in configuration, not in source**, so a domain expert can review and revise it without reading code — and compose it fail-fast, so a missing fragment breaks the boot rather than silently shipping a prompt with a hole in it.
- **Separate the lanes:** domain-owned content (terminology, interpretation, conduct) in files the domain expert edits; engineering-owned orchestration and safety rules in code. Say which lane a change belongs to.

## Decisions & docs

- Grill the load-bearing choices before building (use **grill-with-docs**, which records them as ADRs + a glossary as you go); capture **deferred/blocked** decisions as short ADRs (status *Proposed*, a recommendation as a *lean* not a verdict — the human decides).
- Living docs carry a **Created / Last-edited** header with a per-edit change-log. Reports are self-contained and claim only what is machine-verified; flag the rest for human review.
- **Dated reports are immutable snapshots.** When a later finding invalidates a planning doc, patch the **planning** doc (dated) and leave the snapshot as the record of what was known when. Do not rewrite history to look consistent.
- **Task reports, scaled to the task.** **Sizing:** XS/S = one file, no interface/contract/behaviour change; **M/L = anything else** — several files, a new module or config surface, a changed public interface or contract, or a call someone could reasonably disagree with. M/L and decision-shaped work produces a report under `docs/reports/` (named `YYYY-MM-DD-<slug>.md`, from the repo's `docs/reports/_TEMPLATE.md`): the task, the **decision-making process** (options, choices, who decided), what was done, evidence, and **outstanding items** — enough that a collaborator can pick the work up cold. For XS/S changes, a well-filled PR description is the report; do not manufacture ceremony for a one-line change. Be honest about what is not done.
- **Reconcile the tracker and the docs in both directions.** The board holds items the docs missed, and vice versa. When syncing, expect to learn in both directions and say which way each item moved.

## Red flags — STOP

- About to commit / push / open a PR — or post, comment, message, deploy — without asking.
- Bundling unrelated changes into one PR.
- "It's too small to test / template / ask."
- Claiming "done", "passing", or "fixed" without having run it — or while CI is red or missing.
- Building something because a doc or ticket says it is missing, without checking the code.
- Reviewing only the diff's logic — never asking whether it works where it ships, or trusting a library's default from memory instead of reading its installed source.
- Self-reviewing silently because the reviewer was unavailable.
- Implementing a review finding without verifying it — or dismissing one without evidence.
- Quoting the measurement that supports the choice while a contradicting one sits in the same table.
- Adding a config key, flag, or option that nothing reads.
- Shipping code with no docstrings, or leaving the README stale after a behavior change.
- Silencing the linter (blanket `# noqa`, disabling rules) to go green instead of fixing the code or the style standard.
- Backticks inside a `-m`/`--body` string.

Each of these means: stop, scope down, verify, and hand the gate back to the human.
