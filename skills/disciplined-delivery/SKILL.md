---
name: disciplined-delivery
description: Use when implementing a feature, bugfix, or change in a repo that ships work as small, human-reviewed pull requests — especially before committing, branching, pushing, or opening a PR.
---

# Disciplined Delivery

## Overview

Ship work as **small, test-first, individually reviewable increments**, and let the **human** be the gate that commits and merges. Optimise for a reviewer who reads every diff — not for speed of landing code.

**Core principle:** one focused change, proven green, presented for review — then ask before any git write.

This skill does not reinvent planning or testing discipline: **planning and brainstorming run through the `superpowers` plugin** (`brainstorming`, `writing-plans`), and so does **test-driven development** (`test-driven-development`) and final verification (`verification-before-completion`). This skill orchestrates them and owns the review-gate discipline around them.

## Requires

This skill leans on companion skills and does not reimplement them:

- **`superpowers`** (obra) — declared as a plugin dependency in `plugin.json`, so Claude Code installs it automatically. Provides `brainstorming`, `writing-plans`, `test-driven-development`, and `verification-before-completion`, used in the loop below.
- **`grill-me`** (mattpocock/skills) — a relentless interviewing skill that stress-tests load-bearing decisions. It ships via `skills.sh`, not as a Claude Code plugin, so it cannot be a machine-resolved `plugin.json` dependency. Install it once with `npx skills@latest add mattpocock/skills` (select `grill-me`).

## When to use

- Implementing any feature, bugfix, refactor, or docs change.
- Before `git commit`, `git push`, creating a branch, or opening a PR.

Not for: throwaway spikes, or repos with no review process (still verify before claiming done).

**Companion:** starting a brand-new agentic/RAG LLM app? Bootstrap the structure once with the sibling `scaffold-agentic-app` skill (in this plugin, invoked as `/disciplined-delivery:scaffold-agentic-app`), then return here and build every feature as a small, reviewed increment.

## The loop (per change)

1. **Think first — plan and brainstorm via `superpowers`.** Ambiguous goal or load-bearing decision? Before coding, brainstorm and plan using the **superpowers** plugin (**REQUIRED:** `superpowers:brainstorming` for non-trivial design; `superpowers:writing-plans` for multi-step work), and use **grill-me** to stress-test any load-bearing decision before you commit to it. Simplest thing that works — no speculative abstraction, no drive-by refactors.
2. **TDD, red-first — via `superpowers`.** Drive the change test-first using the **superpowers** plugin's TDD discipline (**REQUIRED:** `superpowers:test-driven-development`). Watch the test fail for the right reason, then write the minimal code to green.
3. **Verify** (**REQUIRED:** superpowers:verification-before-completion). Full test suite + linter green **locally**, and the **CI pipeline green** on the pushed branch — local-only green is not "done". The lines you touched are covered. Claim only what you actually ran.
4. **Stop and ask.** Leave the result as uncommitted working-tree changes, summarise, and **ask before any git write** (branch / commit / push / PR). Reading, editing, and running tests need no permission; git-writes do.

## Branch & PR conventions

- One branch = one focused change. Name it `feat/…`, `fix/…`, `chore/…`, `docs/…`, `test/…`; target the default branch.
- **Avoid stacked PRs.** If a series is unavoidable, keep each off the default branch and merge **bottom-up**, letting the host retarget the next before merging it.
- **The PR template is mandatory.** This repo uses [`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md) (adapted from obra/superpowers). Fill **every** section honestly — who submitted (model/harness/human reviewer), the real problem, what changed, whether it suits this plugin, **alternatives considered**, whether it bundles unrelated changes, existing-PR check, environment tested, **skill auto-trigger transcript** if you added/changed a skill, evaluation, the Rigor checkboxes, and the human-review checkbox. Blank sections, placeholder text, bundled changes, or no evidence of human review get the PR closed without review.
- **Skills are code, not prose.** Changing a skill's behavior-shaping wording requires adversarial testing and eval evidence (use `superpowers:writing-skills`), per the template's Rigor section — not just a happy-path check.

## Commit hygiene

- Conventional subject (`type(scope): summary`); body explains *why*.
- **Never put backticks or `$(…)` inside `git commit -m "…"` or `gh … --body "…"`** — the shell runs them as command substitution, mangling the message and possibly your environment. Use a quoted heredoc (`git commit -F - <<'EOF' … EOF`) or `--body-file`.
- End with any required trailer (e.g. `Co-Authored-By:`).

## Engineering standards

Every repo this skill ships into is held to these — they are part of "done", not optional polish:

- **A CI pipeline exists and gates merges.** There is a `.github/workflows/` (or equivalent) pipeline that runs the test suite, linter, and any project-specific validation (e.g. manifest/schema checks) on every push and PR. A change is not done until CI is **green** on the branch; a red or *absent* pipeline is a blocker, not a footnote. New repos without CI: add it as part of the first change.
- **A professionally written README.** Clear and current: what the project is, how to install/run it, how to develop and test it (the exact commands CI runs), and the project layout. No stale instructions, no placeholder text. Update it in the same change that changes behavior.
- **Documentation, including docstrings.** Public modules, classes, and functions carry docstrings that say what they do and why — not restatements of the signature. Non-obvious decisions get a comment or an ADR. Keep docs in sync with the code in the same commit; out-of-date docs are a bug.
- **Project memory (`CLAUDE.md`).** Maintain a `CLAUDE.md` at the repo root holding agent instructions and project conventions (how to build/test, where things live, working principles). Keep it current as conventions change.

## Decisions & docs

- Grill the load-bearing choices before building (use **grill-me**); record **deferred/blocked** decisions as short ADRs (status *Proposed*, a recommendation as a *lean* not a verdict — the human decides).
- Living docs carry a **Created / Last-edited** header with a per-edit change-log. Reports are self-contained and claim only what is machine-verified; flag the rest for human review.

## Red flags — STOP

- About to commit / push / open a PR without asking.
- Bundling unrelated changes into one PR.
- "It's too small to test / template / ask."
- Claiming "done", "passing", or "fixed" without having run it — or while CI is red or missing.
- Shipping code with no docstrings, or leaving the README stale after a behavior change.
- Backticks inside a `-m`/`--body` string.

Each of these means: stop, scope down, verify, and hand the gate back to the human.
