---
name: disciplined-delivery
description: Use when implementing a feature, bugfix, or change in a repo that ships work as small, human-reviewed pull requests — especially before committing, branching, pushing, or opening a PR.
---

# Disciplined Delivery

## Overview

Ship work as **small, test-first, individually reviewable increments**, and let the **human** be the gate that commits and merges. Optimise for a reviewer who reads every diff — not for speed of landing code.

**Core principle:** one focused change, proven green, presented for review — then ask before any git write.

## When to use

- Implementing any feature, bugfix, refactor, or docs change.
- Before `git commit`, `git push`, creating a branch, or opening a PR.

Not for: throwaway spikes, or repos with no review process (still verify before claiming done).

**Companion:** starting a brand-new agentic/RAG LLM app? Bootstrap the structure once with the `scaffold-agentic-app` skill, then return here and build every feature as a small, reviewed increment.

## The loop (per change)

1. **Think first.** Ambiguous goal or load-bearing decision? Ask / brainstorm before coding (**REQUIRED:** superpowers:brainstorming for non-trivial design; superpowers:writing-plans for multi-step work). Simplest thing that works — no speculative abstraction, no drive-by refactors.
2. **TDD, red-first** (**REQUIRED:** superpowers:test-driven-development). Watch the test fail for the right reason, then minimal code to green.
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

- Grill the load-bearing choices before building; record **deferred/blocked** decisions as short ADRs (status *Proposed*, a recommendation as a *lean* not a verdict — the human decides).
- Living docs carry a **Created / Last-edited** header with a per-edit change-log. Reports are self-contained and claim only what is machine-verified; flag the rest for human review.

## Red flags — STOP

- About to commit / push / open a PR without asking.
- Bundling unrelated changes into one PR.
- "It's too small to test / template / ask."
- Claiming "done", "passing", or "fixed" without having run it.
- Backticks inside a `-m`/`--body` string.

Each of these means: stop, scope down, verify, and hand the gate back to the human.
