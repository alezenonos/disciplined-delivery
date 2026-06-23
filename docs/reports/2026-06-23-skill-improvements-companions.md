# Report: Swap grill-me → grill-with-docs, add code-review-skill, apply writing-great-skills

| | |
|---|---|
| Date created | 2026-06-23 |
| Last edited | 2026-06-23 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | builds on PR #1, PR #2 (both merged); branch `claude/agentic-systems-structure-qef42e` |

## Task

Three requests, in one task:
1. *"the disciplined-delivery skill should call awesome-skills/code-review-skill to review the
   code just before / when the user asks to proceed with a PR. So there is a dependency on
   this as well."*
2. *"use mattpocock's writing-great-skills SKILL.md to improve our skills."*
3. *"we can replace grill-me with grill-me-with-docs if possible."*

**Goal (restated):** add a pre-PR code-review gate (and declare the dependency), swap the
grilling companion for its docs-producing variant, and tighten our skills using the
writing-great-skills principles.

## Context

The plugin already declared `superpowers` (plugin dep) and `grill-me` + (pending)
`code-review-skill` as companions. `grill-me-with-docs` does not exist by that name; the real
skill is **`grill-with-docs`** at `mattpocock/skills/skills/engineering/grill-with-docs` — the
codebase-oriented grilling variant that writes ADRs + a glossary (`CONTEXT.md`) as it goes,
which pairs naturally with this skill's "Decisions & docs" ADR guidance.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Grilling companion | `grill-me` / `grill-with-docs` | `grill-with-docs` | The "with-docs" skill the user meant; produces ADRs+glossary, aligns with Decisions & docs | Human (agent corrected the exact name) |
| `code-review-skill` classification | plugin.json dep / companion | Companion (git clone) | It's a bare skill (clone into `~/.claude/skills/`), not a marketplace plugin — a dep entry would `dependency-unsatisfied` | Agent |
| Code-review trigger point | always / at PR time | At PR time (loop step 4, on human approval to proceed) | Matches the request; keeps the loop cheap until a PR is actually wanted | Human |
| writing-great-skills scope | full restructure / surgical | Surgical (tighten description; collapse duplicated PR-template enumeration to a single-source pointer; leave tuned loop/red-flags wording) | Our own "skills are code" standard requires evals before rewriting behavior-shaping wording | Agent (flagged) |
| scaffold-agentic-app | edit / leave | Leave | Already conforms (progressive disclosure to `references/structure.md`, checkable steps, trigger-rich description) | Agent |

## What was done

- **`disciplined-delivery` SKILL.md**:
  - Requires: `grill-me` → `grill-with-docs`; added `code-review-skill` (git-clone companion).
  - Loop step 1: grilling now via `grill-with-docs`.
  - Loop step 4: on approval to open a PR, **run `code-review-skill` over the diff** and
    resolve blocking/important findings first.
  - PR-template bullet collapsed from a full re-enumeration to a **single-source pointer** to
    `.github/PULL_REQUEST_TEMPLATE.md` (writing-great-skills: kill duplication / single source
    of truth).
  - Description tightened ("a feature, bugfix, or change" → "a change" — one branch, not three).
  - Decisions & docs: grilling via `grill-with-docs` (records ADRs+glossary inline).
- **README**: companion install steps (grill-with-docs + code-review-skill), the
  what-gets-installed table, and the Mermaid diagram (grilling label + a new "Code review the
  diff" node before the human-review gate). Diagram re-validated (`valid: true`).
- **install.sh**: prints both companion-skill steps instead of the single grill-me step.

## Verification / evidence

- `python scripts/validate_manifests.py` → passes.
- `claude plugin validate .` → passes.
- Updated Mermaid diagram validated via the renderer → `valid: true`.
- Confirmed (web) that `grill-with-docs` exists at `mattpocock/skills/skills/engineering/`
  and `code-review-skill` is a git-clone bare skill (no marketplace).

**Not done:** no clean-session auto-trigger transcript; no adversarial/eval evidence for the
skill-text edits (same standing rigor gap).

## Outstanding / next steps

1. **Open a PR** for branch `claude/agentic-systems-structure-qef42e` (this change is unmerged).
2. **Deeper writing-great-skills pass** (deferred): progressive-disclose `Engineering standards`
   / `Commit hygiene` to external reference files; a leading-word pruning pass. Deferred because
   it rewrites behavior-shaping content and our own standard requires adversarial/eval evidence.
3. **Auto-trigger transcripts + adversarial eval** for the skill edits (recurring gap).
4. Companions install separately and are not machine-resolved: `grill-with-docs`
   (`npx skills@latest add mattpocock/skills`) and `code-review-skill` (`git clone`).

## References

- writing-great-skills: https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md
- grill-with-docs: https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
- code-review-skill: https://github.com/awesome-skills/code-review-skill

## Change log

- 2026-06-23: created.
