# Report: Measure and gate repo-wide coverage in CI

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | ale_zenonos@hotmail.com |
| Status | Done — merged in PR #22; badge intentionally skipped |
| Related | PR #22 (merged); follows merged PRs #19, #20, #21 |

## Task

The human asked for "coverage tooling + a badge" for the repo. This change delivers the
**tooling** half: the repo's own code (`scripts/`, the scaffold generator) is now measured
for coverage in CI and gated on a threshold. The badge is deferred to a separate decision
(see Outstanding) because it carries a third-party-vs-CI-commit-back trade-off.

## Context

PR #21 added a coverage gate for the `examples/` app, but the repo's **own** tooling had no
coverage measurement at all. A first attempt reported 0% because the repo's `tests/` invoke
the scripts as **subprocesses** (`subprocess.run([sys.executable, ...])`), which in-process
coverage does not see. The fix is coverage's documented subprocess support: set
`COVERAGE_PROCESS_START` so the child processes start measuring, and run coverage in
`parallel` mode so per-process data is combined. With that, real coverage is **88%**
(`check_evals.py` 90%, `validate_manifests.py` 82%, `scaffold.py` 94%).

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Measure repo coverage at all | yes / no | Yes | Human asked for coverage tooling; subprocess support makes it feasible (88%) | Human |
| Subprocess coverage | `COVERAGE_PROCESS_START` + parallel / refactor tests to in-process | Env + parallel | No test rewrite; coverage's standard mechanism; surgical | Agent |
| Threshold | 88 (exact) / 85 (headroom) | 85 | Small headroom so trivial matrix differences don't flip the gate red, while still meaningful | Agent |
| Config location | `.coveragerc` / `pyproject.toml` | `pyproject.toml` | The repo already centralises ruff + pytest config there | Agent |
| Badge | add one / skip | Skip | The `fail_under=85` gate is the real signal; no built-in GitHub coverage badge exists, and the alternatives (third-party service / CI commit-back) aren't justified. Reaffirmed after the repo went public | Human |

## What was done

- `pyproject.toml` — added `[tool.coverage.run]` (`parallel`, `source`) and
  `[tool.coverage.report]` (`fail_under = 85`, `show_missing`).
- `.github/workflows/ci.yml` — the unit-test step now runs `pytest --cov` with
  `COVERAGE_PROCESS_START` exported so subprocess coverage is captured and gated.
- `README.md` — the Development section documents the coverage command and why the env var
  is needed.

## Verification / evidence

Run locally exactly as CI runs it:

- `COVERAGE_PROCESS_START="$PWD/pyproject.toml" pytest -q --cov --cov-report=term-missing` →
  **13 passed; TOTAL 88% (87.50%); "Required test coverage of 85.0% reached" (exit 0)**.
- `ruff check .` → clean. `ci.yml` parses as valid YAML.

Not yet verified in CI across the 3.10–3.13 matrix — pending the PR run.

## Outstanding / next steps

- **Coverage badge (the other half of the ask) — decided: NOT added.** The human chose to
  rely on the CI gate rather than add a badge. Rationale: the build-enforced `fail_under = 85`
  gate is the real coverage signal, and GitHub has no built-in coverage badge — the only ways
  to add one are a third-party service (discouraged by this repo's PR template) or a CI
  commit-back step (extra `contents: write` + workflow complexity), neither judged worth it.
  Decision reaffirmed after the repo was made public (2026-06-25): going public removed the
  earlier "a badge wouldn't render for logged-out viewers" concern, but the gate-is-the-signal
  rationale stands on its own, so the badge stays skipped. No follow-up needed.
- Coverage of the example app stays a separate 100% gate (PR #21); this gate covers the
  repo's own tooling.

## References

- Merged PRs #19, #20, #21.
- coverage.py subprocess measurement docs (`COVERAGE_PROCESS_START`, `parallel`).

## Change log

- 2026-06-25: created; repo-wide coverage measured (88%) and gated at 85% in CI.
- 2026-06-25: merged as PR #22; recorded the human's decision to skip the coverage badge.
- 2026-06-25: repo made public; badge decision reaffirmed (skip), stale "private repo"
  rationale corrected.
