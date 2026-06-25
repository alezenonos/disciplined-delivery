# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/alezenonos/disciplined-delivery/compare/disciplined-delivery--v0.2.1...HEAD
[0.2.1]: https://github.com/alezenonos/disciplined-delivery/compare/disciplined-delivery--v0.2.0...disciplined-delivery--v0.2.1
[0.2.0]: https://github.com/alezenonos/disciplined-delivery/compare/disciplined-delivery--v0.1.0...disciplined-delivery--v0.2.0
[0.1.0]: https://github.com/alezenonos/disciplined-delivery/releases/tag/disciplined-delivery--v0.1.0
