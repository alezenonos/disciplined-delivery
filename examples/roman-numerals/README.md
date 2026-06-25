# Example: Roman numerals (a `disciplined-delivery` walkthrough)

A deliberately tiny app — convert an integer (1–3999) to a Roman numeral —
included as a **worked example of the `disciplined-delivery` skill**, not as a
feature of the plugin itself. It shows what "one focused, test-first,
reviewable increment" looks like end to end.

## What's here

| File | Role |
|------|------|
| `roman.py` | The library: `to_roman(number) -> str`, with range/type validation. |
| `cli.py` | A one-argument CLI wrapper: `python cli.py 1954` → `MCMLIV`. |
| `test_roman.py` | The pytest suite that drove the library. |
| `test_cli.py` | Tests for the CLI wrapper (added when coverage showed it was untested). |

## Run it

```bash
cd examples/roman-numerals
python cli.py 2024          # -> MMXXIV
python -m pytest -q         # 29 passed
ruff check .                # clean

# with the coverage gate CI enforces (100% of roman.py + cli.py):
pip install pytest-cov
python -m pytest -q --cov=roman --cov=cli --cov-report=term-missing --cov-fail-under=100
```

> The example stays out of the repo's own `pytest` (`testpaths = ["tests"]`)
> so it can't perturb the plugin's unit tests, but CI **does** run this suite
> as a dedicated step with the 100% coverage gate above — see
> `.github/workflows/ci.yml`.

## How this followed the skill

- **Think first / simplest thing.** A pure function plus a thin CLI — no
  config, no classes, no speculative `from_roman` that nobody asked for.
- **TDD, red-first.** `test_roman.py` was written first and failed with
  `ModuleNotFoundError: No module named 'roman'` before any implementation
  existed; the known-value, out-of-range, and non-int cases then drove
  `to_roman` to green.
- **Verify.** Full suite green locally (29 passed, 100% line coverage of
  `roman.py` + `cli.py`) and `ruff check .` clean across the whole repo.
- **Docstrings + README.** Public function and module documented with *why*
  (the 1–3999 bound, the `bool` rejection), not a restatement of the signature.
- **Stop and ask.** Built in the working tree and handed back for review
  before any git write — the human is the commit/merge gate.

See `docs/reports/2026-06-25-roman-numerals-example.md` for the full task
report.
