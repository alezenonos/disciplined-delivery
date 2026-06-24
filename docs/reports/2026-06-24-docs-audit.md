# Report: Documentation audit + critical assessment of engineering gaps

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | follows PRs #1–#3 (merged); branch `claude/agentic-systems-structure-qef42e` |

## Task

*"Audit documentation, inline and otherwise including readme and diagrams, and update to
reflect the latest changes. Critically assess and let me know if something is missing for
professional software engineering with Claude Code."*

## Context

After three merged PRs (plugin packaging, CI/standards/CLAUDE.md/reports, code-review gate +
grill-with-docs), some docs predated later changes and could have drifted.

## What was done (doc sync)

Audited every surface against the current repo state:

- **README** — `Layout` block was stale (missing `CLAUDE.md`, `README.md`, `install.sh`,
  `docs/reports/`); added them. `How it works` prose now mentions the `code-review-skill`
  step and the `docs/reports/` entry. Mermaid diagram already current (grill-with-docs +
  code-review node).
- **CLAUDE.md** — `Layout` now lists `docs/reports/`; `How to work here` now reflects the full
  workflow: grilling via `grill-with-docs`, the pre-PR `code-review-skill` gate, and the
  per-task report requirement.
- **Verified no drift** — `skills/scaffold-agentic-app/references/structure.md` and the skill's
  "What it produces" match the generator's actual 58-file output (regenerated and diffed).
  Inline docstrings in `scaffold.py` and `scripts/validate_manifests.py` are accurate.
  Remaining `grill-me` mentions live only in prior reports (correct — point-in-time records).

## Verification / evidence

- Regenerated the scaffold and confirmed the tree matches the documented structure.
- `python scripts/validate_manifests.py` and `claude plugin validate .` pass.
- Repo-wide grep: no stale `grill-me` / `four commands` references in live surfaces.

## Critical assessment — gaps for professional software engineering with Claude Code

Honest gaps, roughly prioritised. None are blocking; several need a maintainer decision.

1. **No LICENSE** (high). Public repo that attributes/links third-party skills, with no
   license file. Pick one (MIT mirrors the companions).
2. **The repo doesn't test its own code** (high). `scaffold.py` and `validate_manifests.py`
   have no committed unit tests; CI exercises them indirectly (generate/compile/pytest the
   *generated* app, plus an ad-hoc negative test). The skill demands tests — the repo should
   hold itself to it with a `tests/` suite.
3. **No linter runs, though the skill requires "linter green"** (high/medium). No `ruff`
   (or equivalent) config or CI step over this repo's Python. The standard is stated but
   unenforced here.
4. **No skill-behavior evaluation** (medium, recurring). Skills are behavior-shaping, the PR
   template demands auto-trigger transcripts + adversarial evals, but there is no harness or
   captured evidence. This is the most-deferred item across the session.
5. **No CONTRIBUTING.md** (medium). The PR template implies external contributors; a short
   contributing guide + local-dev pointer would complete the on-ramp.
6. **No CHANGELOG / release-versioning policy** (medium). `plugin.json` is pinned at `0.1.0`;
   no changelog or `claude plugin tag` release flow, so marketplace consumers can't track
   what changed between versions.
7. **CI supply-chain hygiene** (low/medium). Actions are tag-pinned (`@v4`/`@v5`), not
   SHA-pinned; single Python version (3.11) though the scaffold targets `>=3.10`.
8. **No markdown link-checking** (low). Many cross-file/external links; nothing guards against
   rot.

## Outstanding / next steps

1. Open a PR for this doc-sync (branch is unmerged).
2. Decide which assessment items to action — I'd start with **LICENSE**, a **`tests/` suite +
   `ruff` in CI**, and **CONTRIBUTING.md**; then a **CHANGELOG** + release policy.
3. Still open from earlier: skill auto-trigger transcripts + adversarial eval evidence.

## References

- This repo's CI: `.github/workflows/ci.yml`; standards in `skills/disciplined-delivery/SKILL.md`.
- Plugin versioning/tagging: https://code.claude.com/docs/en/plugin-dependencies

## Change log

- 2026-06-24: created.
