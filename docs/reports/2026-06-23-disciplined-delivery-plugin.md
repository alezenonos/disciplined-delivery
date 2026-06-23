# Report: Package disciplined-delivery as an installable plugin (+ scaffolder, standards, docs)

| | |
|---|---|
| Date created | 2026-06-23 |
| Last edited | 2026-06-23 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | PR #1 (merged); branch `claude/agentic-systems-structure-qef42e` (3 commits unmerged → needs PR #2) |

## Task

The session began with a shared reference-architecture diagram for a production RAG/agentic
app and the question: *"does this structure make sense… can we make a file supplementary to
the skill that can be invoked to make this file structure with placeholder code?"* It then
grew, across several follow-ups, into: package the repo as an installable Claude Code plugin;
declare its skill dependencies; make installation easy; adopt obra/superpowers' PR template;
add a CI pipeline and engineering standards; add a `CLAUDE.md` with Karpathy-style
principles; and establish this `docs/reports/` convention.

**Goal (restated):** turn a single-file skill repo into a professionally packaged,
installable plugin with a scaffolder, enforced standards, and a documented decision trail.

## Context

The repo started as one root `SKILL.md` (`disciplined-delivery`) — a methodology skill with
no install path, no companion tooling, and no declared link to the `superpowers` skills it
already marked "REQUIRED". `main` now contains the merged PR #1 (plugin packaging through the
PR template). This branch adds CI/standards, the manifest validator, the `CLAUDE.md`, and
this reporting convention on top.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Scaffolder form | New companion skill / bundled script / markdown-only | New companion skill | Independently invocable, discoverable | Human |
| Scaffold stack | Python/FastAPI/RAG / stack-agnostic | Match the diagram (Python) | Fidelity to the shared design; fill its gaps | Human |
| Stub depth | Light runnable stubs / empty files / full example | Light runnable stubs | Boots, but no speculative logic | Human |
| Skill exposure | Sibling-skill restructure / keep bundled / **convert to plugin** | Convert repo to a plugin | True namespaced, independently-invocable skills | Human |
| grill-me source | mattpocock/skills / part of superpowers / intent-only | mattpocock/skills | That's where grill-me actually lives | Human |
| grill-me install | Vendor into plugin / keep external | Keep external | Avoid redistributing/forking a third-party skill | Human |
| PR template branch policy | Target `main` / adopt a `dev` branch | Target `main` | Repo has no dev branch | Human |
| PR template fidelity | Adapt wording / near-verbatim | Adapt to this repo | Superpowers-specific bits (core library, bootstrap test) don't transfer | Human |
| CI manifest check | `claude plugin validate` in CI / stdlib validator | stdlib validator (script) | Hermetic CI, no CLI/auth/network dependency | Agent |
| grill-me as `plugin.json` dep | Declare it / document it | Document only | It's not a marketplace plugin → would `dependency-unsatisfied` and disable the plugin | Agent |
| Karpathy principles | Invent / use canonical distillation | Use & attribute the Forrest Chang / multica-ai distillation | Faithful, not fabricated quotes | Agent |

## What was done

- **Scaffolder skill** (`skills/scaffold-agentic-app/`): idempotent `scaffold.py` generating a
  58-file RAG/agentic app tree with light stubs; `SKILL.md`; `references/structure.md`.
  (commit `87aa2ae`)
- **Plugin layout**: `.claude-plugin/plugin.json`; moved root `SKILL.md` →
  `skills/disciplined-delivery/SKILL.md`; bundled script referenced via `${CLAUDE_SKILL_DIR}`.
  (`bf0626b`)
- **Dependencies**: declared `superpowers` (cross-marketplace) in `plugin.json`; documented
  `grill-me` as a `skills.sh` companion. (`b1b34bf`)
- **Marketplace**: `.claude-plugin/marketplace.json` (`alezenonos`, `source: "./"`,
  `allowCrossMarketplaceDependenciesOn: ["superpowers-marketplace"]`). (`0f193ab`)
- **Install UX**: `README.md` guide + `install.sh`. (`9ac1946`)
- **PR template**: `.github/PULL_REQUEST_TEMPLATE.md` adapted from obra/superpowers; skill
  points at it as mandatory. (`c12339e`) — merged via **PR #1** (`cca1534`).
- **CI + standards**: `.github/workflows/ci.yml`, `scripts/validate_manifests.py`, and an
  "Engineering standards" section in the skill (CI-green = done, professional README,
  docstrings). (`c53fb5b`)
- **Project memory**: `CLAUDE.md` with Karpathy-derived principles; skill now requires it.
  (`8a83ae8`)
- **Reporting**: this `docs/reports/` convention + template (current commit).

## Verification / evidence

**Verified locally:**
- `python scripts/validate_manifests.py` → passes; correctly **fails** on a broken manifest
  (negative test).
- `claude plugin validate .` → passes, no warnings.
- Scaffold self-test: 58 files generated, `compileall` clean, re-run idempotent (0 created),
  generated app `pytest` green (stubs skipped), app imports with `/chat` + `/health`.
- **Live end-to-end install** (against the local checkout): adding obra's marketplace then
  installing this plugin reported **"+ 1 dependency: superpowers"**; both plugins enabled,
  zero errors; the four superpowers skills present; installed `scaffold.py` runs. Cleaned up.

**Not yet verified:**
- CI is **not** confirmed green on GitHub Actions (only reproduced locally) — runs on PR/main.
- No clean-session transcript proving the skills **auto-trigger**.
- No adversarial/eval evidence for the skill-wording changes.

## Outstanding / next steps

For a collaborator (or the next session) to pick up:

1. **Open PR #2** for branch `claude/agentic-systems-structure-qef42e` (3 commits ahead of
   `main`: CI/standards, validator, CLAUDE.md, reports). It was not opened pending the
   human's go-ahead.
2. **Confirm CI is green on GitHub** once the PR runs it — required by the new "done" bar.
3. **Capture skill auto-trigger transcripts** (disciplined-delivery on an "implement a small
   feature" prompt; scaffold-agentic-app on a "scaffold an agentic app" prompt) — the PR
   template requires these for skill changes.
4. **Adversarial / eval evidence** for the behavior-shaping skill edits (use
   `superpowers:writing-skills`).
5. **Decide whether to split** the large bundle into separate PRs (flagged on PR #1; the
   methodology prefers it).
6. Note for users: the cross-marketplace `superpowers` dependency resolves only if obra's
   marketplace is added first; `grill-me` is a separate (interactive) `skills.sh` install.

## References

- PR #1: https://github.com/alezenonos/disciplined-delivery/pull/1
- obra/superpowers + marketplace: https://github.com/obra/superpowers , https://github.com/obra/superpowers-marketplace
- grill-me (mattpocock/skills): https://github.com/mattpocock/skills
- Karpathy-derived CLAUDE.md: https://github.com/multica-ai/andrej-karpathy-skills
- Claude Code skills/plugins docs: https://code.claude.com/docs/en/skills , https://code.claude.com/docs/en/plugins-reference

## Change log

- 2026-06-23: created; covers work through commit `8a83ae8` plus this reporting convention.
