# Report: Verify the roman-numerals example in CI with a coverage gate

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | ale_zenonos@hotmail.com |
| Status | In progress (awaiting CI + human merge) |
| Related | branch `test/example-cli-coverage-ci`; follows merged PRs #19, #20 |

## Task

The human asked whether the example had a coverage badge, whether CI actually ran for it,
and whether it followed docstring/best-practice standards. Investigation found two real gaps;
the human chose to (a) wire the example's tests into CI and (b) measure coverage in CI.
Goal: make the example genuinely CI-verified, with coverage measured and gated.

## Context

The example (`examples/roman-numerals/`, merged in #19) had 23 passing tests — but run
**locally only**. The repo's `pytest` is scoped by `testpaths = ["tests"]`, so CI never
executed the example's suite; CI's `ruff check .` (whole-repo) was the only check that
touched it. Separately, the repo measured no coverage at all.

Two findings surfaced while investigating:

1. **The example's tests never ran in CI** — green locally, unverified by the pipeline.
2. **`cli.py` had zero test coverage** — the 23 tests exercised only `roman.py`. Coverage
   measurement is exactly what revealed this.

A third finding shaped the scope: the repo's own `tests/` invoke code as **subprocesses**
(`subprocess.run([sys.executable, ...])`), so in-process coverage reports 0% for them.
Whole-repo coverage therefore needs subprocess instrumentation (`COVERAGE_PROCESS_START` +
combine), which is fiddly across the 3.10–3.13 matrix — out of scope for this change.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Run example tests in CI | yes / leave local-only | Yes, dedicated CI step | Closes the dogfooding gap; tests that never run in CI aren't "done" per the skill | Human |
| Coverage approach | badge (Codecov) / measure in CI / skip | Measure + gate in CI, no badge | A badge couples to a third-party service the PR template discourages; measurement is the substance | Human |
| Coverage scope | whole repo / example only | Example only (this PR) | Repo `tests/` are subprocess-based (0% in-process); whole-repo coverage is a separate, larger task | Agent |
| `cli.py` gap | add tests / exclude from coverage | Add `test_cli.py` | Coverage found real untested code; the right fix is to test it, not hide it | Agent |
| `__main__` guard line | pragma / write an exec test | `# pragma: no cover` | The thin entrypoint is exercised via `main()`; a subprocess test just to cover one line is not worth it | Agent |

## What was done

- `examples/roman-numerals/test_cli.py` — new: covers every branch of `main` (success, both
  error exits, the argument-count guard), via `capsys` and exit codes.
- `examples/roman-numerals/cli.py` — added `# pragma: no cover` to the `__main__` guard.
- `.github/workflows/ci.yml` — installs `pytest-cov`; adds an "Example tests with coverage
  gate" step running the example suite with `--cov=roman --cov=cli --cov-fail-under=100`.
- `examples/roman-numerals/README.md` — documents `test_cli.py`, the 29-test count, and the
  coverage command CI enforces.

## Verification / evidence

Run locally on the branch:

- `pytest -q --cov=roman --cov=cli --cov-fail-under=100` in the example dir →
  **29 passed; cli.py 100%, roman.py 100%, TOTAL 100%; gate satisfied (exit 0)**.
- `ruff check .` (whole repo) → clean.

Not yet verified in CI: the new CI step runs on the branch's PR — pending.

## Outstanding / next steps

- **Whole-repo coverage is not measured.** The repo's `tests/` are subprocess-based, so
  in-process coverage reports 0%. Adding repo-wide coverage needs subprocess instrumentation
  (`COVERAGE_PROCESS_START` + `coverage combine`) and a sensible threshold measured first —
  a separate change if wanted.
- A companion PR amends the `disciplined-delivery` skill to require coverage measurement
  (done with eval evidence per the skill's Rigor bar), per the human's choice.

## References

- Merged PRs #19 (the example), #20 (README layout).
- `skills/disciplined-delivery/SKILL.md` — step 3 ("the lines you touched are covered").

## Change log

- 2026-06-25: created; added CLI tests, coverage gate, and CI step; verified locally.
