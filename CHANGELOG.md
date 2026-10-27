# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `README.md`: a copy-paste prompt for having an agent install the plugin, and install steps for
  **GitHub Copilot** (CLI, VS Code, cloud agent).
- `scripts/validate_manifests.py`: the install-consistency check now fails when `install.sh` or
  `README.md` never adds the marketplace a dependency resolves from, the drift that left
  0.2.2's docs pointing at the legacy `superpowers-marketplace` while CI stayed green. Only
  Claude Code's own `marketplace add` commands count, so the README's Copilot steps can't
  satisfy it.
- `disciplined-delivery`: **shipped assets** under `skills/disciplined-delivery/assets/`, ready
  to copy into a consuming repo: a lean `PULL_REQUEST_TEMPLATE.md` (problem, change, how
  tested naming the commit, alternatives, known limits, single-change attestation, review
  boxes for behaviour-shaping and shipped changes); `check_pr_template.py` + `pr-template.yml`,
  a CI check that reads its rules from the template (sections present, prose filled, the
  single-change box ticked; a `--must-tick` typo is a config error, not a silent no-op); and
  `ci_local.sh`, which runs the repo's checks on a **temporary clean checkout of the commit**,
  never the working tree, with `--merge-preview` testing the merge with the base and the tested
  SHA printed for the PR body.
- `disciplined-delivery`: `references/gates.md` (what each gate caught and what it costs) and
  `references/evidence.md` (the measurement, evidence and recording norms), so `SKILL.md`
  carries one line per rule and the reasoning lives beside it.
- `disciplined-delivery`: loop gates for **mutation-checking a test that passes at once**
  (and confirming a test still asserts before trusting a survived mutation), **verifying on a
  clean checkout of the exact commit** and naming the SHA, **confirming the artifact under test
  is the one you changed**, and **enumerating a guard's callers and exits** before claiming it
  holds (defaults are paths; `async def` need not suspend; name a bound's zero point; bound the
  final encoded artefact).
- `disciplined-delivery`: **"Measurement & rules"** — measure before adding a rule or check
  ("regression guard" when the count is zero); report, never exclude; state what would falsify
  a measurement; a derived number carries its command; evidence artefacts are immutable.
- `disciplined-delivery`: behaviour-shaping changes now require **two runs on the same
  configuration or no claim**, a subset chosen by whether the change narrows or broadens, a
  confounded baseline disclosed, a release that refuses an unmeasured prompt, and no
  self-authored golden expectations.
- `disciplined-delivery`: engineering standards for **diagnostics that degrade, never abort**,
  **fail-closed privacy settings**, **checks that report PASS/FAIL/BLOCKED with a reason**,
  **release and deploy as reviewed scripts in the repo** with every production change logged
  with its rollback, **specs compared against a partner's source** by a check, and
  **handoffs that need no command from the recipient**.
- `disciplined-delivery`: decisions & docs — **rationale has one home and the code points at
  it** (ADR / report / one-line comment; a decision index; a citation guard), corrections
  marked `[corrected]` in place, the negative report written, a living "how we work" with the
  cost of each gate, and tracker entries that stand on their own.
- This repo dogfoods the assets: `.github/workflows/pr-template.yml` checks PR descriptions
  with the shipped checker; `scripts/ci_local.sh` wraps the shipped runner with CI's commands;
  the PR template gained a "How was it tested?" section; tests cover both assets.
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
- `disciplined-delivery`: the **PR template is now enforced by a check**, not only required by
  prose, and PR bodies must carry the known limits; a gate must render in an enforcing surface
  (template checkbox worded for every case, CI check, or refusing script), kept in proportion
  to what its CI minutes buy, and never a CI path filter.
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

### Fixed
- `assets/ci_local.sh`: the trap-only `cleanup()` now silences both **SC2317** (shellcheck before
  0.11, as on CI's Ubuntu runners) and **SC2329** (0.11+); silencing only SC2329 failed
  shellcheck in CI and in any consuming repo on an older shellcheck.
- `README.md` and `install.sh` add the **official marketplace** (`anthropics/claude-plugins-official`)
  for the `superpowers` dependency; they still pointed at the legacy `superpowers-marketplace`
  after 0.2.2 moved the dependency, leaving `superpowers` unresolved on a fresh install.

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
