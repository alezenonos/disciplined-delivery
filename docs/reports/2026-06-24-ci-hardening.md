# Report: CI hardening — SHA-pinned actions + Python matrix

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | PR B of four sequenced follow-ups (after release-engineering PR #5) |

## Task

Harden CI: pin GitHub Actions to commit SHAs and test across Python versions.

## What was done

- **SHA-pinned actions** with version comments: `actions/checkout@11bd719… # v4.2.2`,
  `actions/setup-python@0b93645… # v5.3.0` (resolved via the GitHub refs API). Removes the
  tag-move risk of floating `@v4`/`@v5`.
- **Python matrix** `3.10–3.13` on the `quality` (lint + tests) and `scaffold` (generator
  self-test) jobs, with `fail-fast: false`. The manifests/shell job stays single-version
  (stdlib + shellcheck are version-agnostic).
- **Least privilege:** top-level `permissions: contents: read`.
- **`.github/dependabot.yml`** (github-actions, weekly) so the SHA pins are maintained rather
  than rotting — the counterpart that makes SHA-pinning sustainable.
- README Layout updated.

## Decisions

| Decision | Chosen | Why |
|----------|--------|-----|
| Pin style | full SHA + `# vX.Y.Z` comment | Security best practice; comment keeps it readable |
| Resolve SHAs | GitHub refs API via WebFetch | The git proxy only allows this repo, so `git ls-remote` of action repos 403s |
| Matrix scope | quality + scaffold only | Manifests/shellcheck don't vary by Python; saves CI minutes |
| Maintain pins | Dependabot weekly | SHA pins without an updater go stale |

## Verification / evidence

`ci.yml` + `dependabot.yml` parse as valid YAML; `ruff` clean; `pytest` → 5 passed;
`validate_manifests` ✓. The matrix itself (esp. the generated app installing on 3.13) is
verified by CI on the PR — see the PR's check runs.

## Outstanding / next steps

- Confirm the 3.10–3.13 matrix is green on the PR (watch CI); if the generated app's deps fail
  on 3.13, narrow the matrix or pin generated `requirements.txt`.
- Remaining follow-ups: **PR C** install smoke test (CLI-auth caveat), **PR D** skill-behavior
  eval harness.

## Change log

- 2026-06-24: created.
