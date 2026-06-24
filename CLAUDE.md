# CLAUDE.md

Project memory for Claude Code and other coding agents working in this repo.

## What this repo is

A Claude Code **plugin**, distributed via a self-hosted marketplace, shipping two skills:

- **`disciplined-delivery`** — ship work as small, test-first, human-reviewed increments.
- **`scaffold-agentic-app`** — scaffold a production RAG/agentic app skeleton.

Layout: `.claude-plugin/` (`plugin.json` + `marketplace.json`), `skills/<name>/SKILL.md`,
`scripts/`, `docs/reports/` (one report per task), `.github/` (CI workflow + PR template).

## How to work here

- **Follow the `disciplined-delivery` skill.** Small focused changes; plan/brainstorm and
  drive TDD through the `superpowers` plugin; grill load-bearing decisions with
  `grill-with-docs`; **stop and ask before any git write**.
- **Before opening a PR, run `code-review-skill` over the diff** and resolve blocking/important
  findings first.
- **Every PR follows** [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
  No bundled or unrelated changes in one PR.
- **Every task leaves a report** under `docs/reports/` (from `_TEMPLATE.md`): decisions,
  what was done, evidence, and outstanding items for a collaborator.
- **This repo dogfoods its own skill.** Changes here follow the `disciplined-delivery` loop —
  including its tests-and-linter-green bar — not just downstream repos the skill is used on.
- **A change is done only when CI is green** — not just locally. Reproduce CI before you
  claim done:
  ```bash
  ruff check . && pytest -q                     # lint + unit tests (this repo's tooling)
  python scripts/validate_manifests.py        # manifests + skill frontmatter
  claude plugin validate .                     # authoritative manifest check
  python skills/scaffold-agentic-app/scaffold.py /tmp/app && python -m compileall -q /tmp/app
  ( cd /tmp/app && pip install -r requirements.txt && pytest -q )
  ```
- **Docs stay in sync.** Public modules, classes, and functions carry docstrings; update the
  README in the same change that changes behavior.

## Working principles (after Andrej Karpathy)

Adapted from Andrej Karpathy's observations on LLM coding pitfalls (distilled by Forrest
Chang — `multica-ai/andrej-karpathy-skills`). They bias toward caution over speed; use
judgment on trivial tasks.

### 1. Think before coding
Don't assume, don't hide confusion, surface tradeoffs. State assumptions explicitly and ask
when uncertain. If multiple interpretations exist, present them — don't pick silently. If a
simpler approach exists, say so. If something is unclear, stop and name what's confusing.

### 2. Simplicity first
Minimum code that solves the problem — nothing speculative. No features beyond what was
asked; no abstractions for single-use code; no unrequested "flexibility" or "configurability";
no error handling for impossible scenarios. If you write 200 lines and it could be 50,
rewrite it. Ask: "would a senior engineer call this overcomplicated?"

### 3. Surgical changes
Touch only what you must; clean up only your own mess. Don't "improve" adjacent code,
comments, or formatting; don't refactor what isn't broken; match the existing style even if
you'd do it differently. Remove imports/variables/functions that *your* change orphaned, but
leave pre-existing dead code (mention it instead). Every changed line should trace directly
to the request.

### 4. Goal-driven execution
Define success criteria, then loop until verified. "Add validation" → "write tests for
invalid inputs, then make them pass." "Fix the bug" → "write a failing test that reproduces
it, then make it pass." "Refactor X" → "ensure tests pass before and after." For multi-step
work, state a brief plan with a verification check per step.

---

Source: <https://github.com/multica-ai/andrej-karpathy-skills> — Karpathy's commentary on LLM
coding pitfalls, distilled into these guidelines.
