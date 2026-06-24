# Report: Install smoke test (hermetic install-consistency check)

| | |
|---|---|
| Date created | 2026-06-24 |
| Last edited | 2026-06-24 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | alezenonos |
| Status | In progress |
| Related | PR C of four sequenced follow-ups (after CI-hardening PR #6) |

## Task

"Make sure it works when downloaded/installed" — add an automated install smoke test.

## Decision: hermetic check, not a live CLI install

A true end-to-end install (`claude plugin marketplace add … && claude plugin install …`) was
**rejected for CI** for two concrete reasons:

1. **Not headless-friendly / unverifiable locally.** The Claude Code CLI likely needs
   auth/interactive context in a bare runner, and this dev environment's git proxy blocks
   cloning third-party repos (obra's marketplace 403s), so a network-based test could not be
   verified green locally before pushing — violating the repo's own "green locally first" rule.
2. The live path was already exercised **manually** during PR #2 (install resolved
   `+ 1 dependency: superpowers`, skills enabled), and the README has a **Verify your install**
   checklist for users.

Instead, this adds a **hermetic install-consistency check** — no network, no CLI, fully
locally verifiable — covering the parts we control that actually break installs.

## What was done

- `scripts/validate_manifests.py` gains `validate_install_consistency()`:
  - every cross-marketplace dependency in `plugin.json` must be listed in
    `allowCrossMarketplaceDependenciesOn` (else a cross-marketplace install is blocked);
  - `marketplace.json` must offer an entry whose name matches `plugin.json`'s name (else the
    plugin can't be installed from its own marketplace).
- `tests/test_validate_manifests.py`: two new tests for those failure modes (7 tests total).
- README "Verify your install" notes the hermetic check.
- Runs in CI already (the existing manifests job) — no workflow change needed.

## Verification / evidence

`ruff` clean; `pytest -q` → 7 passed (incl. the two new failure-path tests); the real repo
passes the new check; `claude plugin validate .` ✓.

## Outstanding / next steps

- **PR D — skill-behavior eval harness** (the last follow-up; the one standard still ungated).
- If a headless `claude plugin install` becomes feasible in CI, add it as an optional job on
  top of this hermetic check.

## Change log

- 2026-06-24: created.
