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
3. **Verify** (**REQUIRED:** superpowers:verification-before-completion). Full test suite + linter green; the lines you touched are covered. Claim only what you actually ran.
4. **Stop and ask.** Leave the result as uncommitted working-tree changes, summarise, and **ask before any git write** (branch / commit / push / PR). Reading, editing, and running tests need no permission; git-writes do.

## Branch & PR conventions

- One branch = one focused change. Name it `feat/…`, `fix/…`, `chore/…`, `docs/…`, `test/…`; target the default branch.
- **Avoid stacked PRs.** If a series is unavoidable, keep each off the default branch and merge **bottom-up**, letting the host retarget the next before merging it.
- **If the repo has a PR template, it is mandatory.** Fill every section honestly: the real problem, what changed, **how it was tested** (the red→green evidence + suite/lint), **alternatives considered** (genuine ones), the single-focused-change checkbox, related PRs. A PR that skips the template gets rejected.

## Commit hygiene

- Conventional subject (`type(scope): summary`); body explains *why*.
- **Never put backticks or `$(…)` inside `git commit -m "…"` or `gh … --body "…"`** — the shell runs them as command substitution, mangling the message and possibly your environment. Use a quoted heredoc (`git commit -F - <<'EOF' … EOF`) or `--body-file`.
- End with any required trailer (e.g. `Co-Authored-By:`).

## Decisions & docs

- Grill the load-bearing choices before building (use **grill-me**); record **deferred/blocked** decisions as short ADRs (status *Proposed*, a recommendation as a *lean* not a verdict — the human decides).
- Living docs carry a **Created / Last-edited** header with a per-edit change-log. Reports are self-contained and claim only what is machine-verified; flag the rest for human review.

## Red flags — STOP

- About to commit / push / open a PR without asking.
- Bundling unrelated changes into one PR.
- "It's too small to test / template / ask."
- Claiming "done", "passing", or "fixed" without having run it.
- Backticks inside a `-m`/`--body` string.

Each of these means: stop, scope down, verify, and hand the gate back to the human.
