# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `disciplined-delivery`: **"Review the whole surface"** — review the deployment paths a change
  ships through (container `COPY`, compose/orchestration env defaults, packaging manifest, CI),
  not just the diff's logic; read a third-party library's installed source when relying on its
  defaults; name what test doubles structurally cannot cover; and disclose in the PR when no
  independent review was possible rather than self-reviewing silently.
- `disciplined-delivery`: **"Receiving review findings"** — verify each finding against the code
  before acting (via `superpowers:receiving-code-review`), fix the cause rather than the symptom,
  record what was deferred and why, and cite the observation that contradicts your own choice.
- `disciplined-delivery`: **"Behaviour-shaping changes (LLM apps)"** — re-run the behavioural eval
  and state the result when prompts, domain rules or model choice change; keep the prompt in
  configuration composed fail-fast; separate the domain-owned and engineering-owned lanes.
- `disciplined-delivery`: loop step **"Establish the ground truth in code"** — grep before building
  something a doc, checklist or ticket claims is missing.
- `disciplined-delivery`: engineering standards for **tests that can fail** (no constant-vs-literal
  tautologies; pin the wiring, not the value), **fail-fast configuration with no dead knobs**
  (unknown keys rejected; never add an option nothing reads), **rot-prone external pins**, and
  **read-only vendor/partner-owned inputs**.

### Changed
- `disciplined-delivery`: the **ask-before-writing gate now covers every outward-visible action**
  — posting to a tracker, commenting, messaging, deploying — not only git writes.
- `disciplined-delivery`: **task reports are now scaled to the task.** Decision-shaped and M/L work
  still gets a `docs/reports/` entry; for XS/S changes a well-filled PR description is the report.
  Sizing is defined inline (XS/S = one file, no interface change) so the relaxation cannot be used
  as an escape hatch. The previous "every task produces a report" rule was heavier than practice
  and was being ignored, which is worse than a smaller rule that is followed.
- `disciplined-delivery`: **reconcile the tracker and the docs in both directions** — expect to
  learn in both, and say which way each item moved.
- `disciplined-delivery`: dated reports are called out as **immutable snapshots** — a later finding
  patches the planning doc (dated) rather than rewriting the snapshot.
- `disciplined-delivery`: the PR-template reference now points at **the consuming repo's**
  `.github/PULL_REQUEST_TEMPLATE.md` instead of a relative path that resolved to this plugin's own
  copy once installed elsewhere.

## [0.2.2] - 2026-07-18

### Changed
- The `superpowers` dependency now resolves from the **official plugin marketplace**
  (`claude-plugins-official`) instead of the legacy `superpowers-marketplace`, which
  stopped receiving updates in June (5.1.0) after superpowers moved to the official
  marketplace (6.x). Unpins consumers from a stale duplicate install.

## [0.2.1] - 2026-06-25

### Changed
- `scaffold-agentic-app`: when the target already has a `CLAUDE.md`/`AGENTS.md`, the generator
  now **appends** its block once (under markers) instead of skipping — a project's own memory is
  preserved, never clobbered.

## [0.2.0] - 2026-06-25

### Added
- Skill evaluation harness under `evals/` (per-skill cases + transcript template) and
  `scripts/check_evals.py`, gated in CI — every skill must have an eval case.
- Hermetic install-consistency check in `scripts/validate_manifests.py` (cross-marketplace
  dependencies must be allow-listed; the marketplace must offer this plugin).
- Python 3.10–3.13 CI matrix; `.github/dependabot.yml` for GitHub Actions.
- `plugin.json` metadata: `homepage`, `repository`, and `license`.

### Changed
- CI actions are SHA-pinned (with version comments) and run under least-privilege
  (`permissions: contents: read`); Dependabot keeps the pins current and groups action
  bumps into one weekly PR.

## [0.1.0] - 2026-06-24

Initial release: the `disciplined-delivery` plugin and its companion scaffolder.

### Added
- **`disciplined-delivery` skill** — ship work as small, test-first, human-reviewed
  increments, with a stop-and-ask git-write gate and a pre-PR `code-review-skill` step.
- **`scaffold-agentic-app` skill** — idempotent generator (`scaffold.py`) for a production
  RAG/agentic app skeleton (Python + FastAPI), with `references/structure.md`.
- **Plugin packaging** — `.claude-plugin/plugin.json` (declares the `superpowers`
  cross-marketplace dependency) and a self-hosting `marketplace.json`.
- **Companions documented** — `grill-with-docs` (mattpocock/skills) and `code-review-skill`
  (awesome-skills), with install steps in the README and `install.sh`.
- **CI** (`.github/workflows/ci.yml`) — ruff lint, pytest unit tests, `shellcheck install.sh`,
  manifest/frontmatter validation, and a scaffold generator self-test.
- **Quality + docs** — `scripts/validate_manifests.py`, `tests/`, `CLAUDE.md` (working
  principles after Karpathy), `.github/PULL_REQUEST_TEMPLATE.md`, the `docs/reports/`
  per-task convention, a usage diagram, `LICENSE` (MIT), `CONTRIBUTING.md`, and `.gitignore`.
