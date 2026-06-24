# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/alezenonos/disciplined-delivery/compare/disciplined-delivery--v0.1.0...HEAD
[0.1.0]: https://github.com/alezenonos/disciplined-delivery/releases/tag/disciplined-delivery--v0.1.0
