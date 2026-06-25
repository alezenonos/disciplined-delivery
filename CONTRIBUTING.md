# Contributing

Anyone contributing to this repo — human or agent — follows the same rules. This repo
**dogfoods its own `disciplined-delivery` skill**: the methodology it ships is the methodology
it is built with.

## The rules (single source of truth)

These live in one place each; read them, don't expect this file to restate them:

- **The loop and review-gate discipline:** [`skills/disciplined-delivery/SKILL.md`](skills/disciplined-delivery/SKILL.md)
  — think first (plan/brainstorm via `superpowers`; grill load-bearing decisions with
  `grill-with-docs`), TDD red-first, verify, then stop and ask before any git write.
- **Project conventions + working principles:** [`CLAUDE.md`](CLAUDE.md).
- **The PR template (mandatory, every section honest):** [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).

## Before you open a PR

1. **One branch = one focused change.** No bundling unrelated changes.
2. **Green locally** (reproduce CI):
   ```bash
   pip install ruff pytest
   ruff check . && pytest -q
   python scripts/validate_manifests.py
   python skills/scaffold-agentic-app/scaffold.py /tmp/app && python -m compileall -q /tmp/app
   ```
3. **Run `code-review-skill` over the diff** and resolve blocking/important findings.
4. **Leave a task report** under [`docs/reports/`](docs/reports/) (from `_TEMPLATE.md`):
   decisions, what changed, evidence, outstanding items.
5. **Fill the PR template** honestly. Blank sections, placeholder text, bundled changes, or no
   evidence of human review get the PR closed without review.
6. **CI must be green** on the branch — local-only green is not "done".

## Skills are code

Changing a skill's behavior-shaping wording requires adversarial testing and eval evidence
(see the PR template's Rigor section), not just a happy-path check. The eval harness lives in
[`evals/`](evals/README.md): cases are validated in CI (`scripts/check_evals.py`), and adding a
skill requires adding its `evals/cases/<skill>.json`. Run the cases and commit a transcript when
you change a skill.

## Releasing (maintainers)

The project follows [Semantic Versioning](https://semver.org/) and keeps a
[`CHANGELOG.md`](CHANGELOG.md). To cut a release:

1. Move the `Unreleased` entries under a new `## [x.y.z] - YYYY-MM-DD` heading.
2. Bump `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) to match.
3. Tag and push using the marketplace convention `<plugin>--v<version>`:
   ```bash
   claude plugin tag --push        # creates disciplined-delivery--v<version>
   ```
   Consumers resolve versioned dependencies against these tags. Every user-facing change
   should add a `CHANGELOG.md` entry under `Unreleased` in the same PR.

## License

By contributing, you agree your contributions are licensed under the repo's [MIT License](LICENSE).
