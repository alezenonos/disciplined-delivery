# Report: repo review and the fixes that followed

| | |
|---|---|
| Date created | 2026-11-10 |
| Last edited | 2026-11-10 |
| Author | Claude Code (cloud session) |
| Human partner | alezenonos |
| Status | In progress: changes made and checked locally; CI has not run on them |
| Related | branch `ccr-94f8b1bc-vmo0co` |

## Task

"Review the repo and suggest improvements", then "Can you fix them all?". The review listed
twelve items; this report records which were fixed, which were not, and why.

## Context

At `2fb7057` the repo was green (ruff clean, 47 tests, 91.5% coverage, manifests valid). The
review's findings were about gaps between what the repo says and what it does: the scaffolder
generated an app that broke the sibling skill's standards, the checks existed in two
hand-kept copies, nothing had been released since 0.2.2, and the validators' failure branches
were untested.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| How to stop CI and local CI drifting | (a) a test comparing the two command lists; (b) one script both call | (b) `scripts/checks.sh`, one group per CI job | The two lists differed in spelling (`pytest` vs `python3 -m pytest`, `$RUNNER_TEMP` vs a scratch dir), so a comparison would be fuzzy. One script cannot drift from itself; job names and the matrix are unchanged. A test fails if the workflow runs a check outside the script. | agent |
| Generated CI: pinned actions go stale inside `scaffold.py` | (a) leave `@v4`; (b) pin and cross-check against this repo's `ci.yml`; (c) pin and generate a `dependabot.yml` | (c) | A SHA pin keeps working when it is old, and the generated repo's own Dependabot bumps it in its first week. (b) would turn every Dependabot PR here red until `scaffold.py` was edited by hand. | agent |
| Model default in the generated app | (a) keep it in `.env.example` and `config.py`; (b) one home | (b) `app/config.py`; `.env.example` keeps a commented override | "A value in more than one place rots." The id was also updated from `claude-opus-4-8` to `claude-opus-5-5`, with a comment that a pinned id must be checked against the provider's list. | agent |
| `extra="forbid"` in generated settings | forbid alone; forbid plus declaring the keys `.env.example` offers | declare them | With forbid alone, the documented first step (`cp .env.example .env`) stopped the app, because three offered keys were undeclared. A generated test now holds the two files together. | agent |
| `claude plugin validate` in CI: pin the CLI? | pin a version; install latest | latest, with the reason in the workflow | Users install the plugin with the current CLI, so a manifest it rejects is broken for them whatever an older validator says. This is the one deliberately unpinned tool. | agent, **for the human to confirm** |
| Version for the release | 0.2.3; 0.3.0 | 0.3.0 | The unreleased section adds shipped assets and many skill gates: features, not patches. | agent, **for the human to confirm** |
| Restructure `SKILL.md` (review item 10) | do it now; defer | deferred | It changes what the agent always has in context. The repo's own rule requires eval evidence for that, and no eval has been run. | agent |

## What was done

- **Scaffolder** (`skills/scaffold-agentic-app/scaffold.py`, its `SKILL.md` and
  `references/structure.md`): `.dockerignore`; settings that reject unknown `.env` keys and
  declare the offered ones; one home for the model default; generated CI with SHA-pinned
  actions, `ruff`, read-only permissions, plus `dependabot.yml`; the repo's lint standard in the
  generated `pyproject.toml` and a docstring on every stub; two generated tests that run
  (`test_config.py`, `test_health.py`); README titled after the target directory;
  `api-reference.md` corrected for `/health`; the unused `app/Dockerfile` removed; a fallback
  sentence for agents that do not set `${CLAUDE_SKILL_DIR}`.
- **Checks**: `scripts/checks.sh` (groups `quality`, `manifests`, `scaffold`), called by
  `.github/workflows/ci.yml` and `scripts/ci_local.sh`; `requirements-dev.txt` with pinned
  tools; a `pip` entry in `.github/dependabot.yml`; `claude plugin validate .` in the
  `manifests` group; matrix moved to Python 3.11–3.14.
- **Validator** (`scripts/validate_manifests.py`): frontmatter read as top-level keys; `name`
  must equal the skill's directory; `plugin.json`'s version must have a `CHANGELOG.md` heading.
- **Tests**: 20 added (47 → 67). Ten are validator tests, most for failure branches that had
  none.
- **Evals**: six more negative prompts for `disciplined-delivery`, mirrored in the pending
  transcript.
- **Release**: `[Unreleased]` became `[0.3.0] - 2026-11-10`; `plugin.json` bumped to `0.3.0`.
- **Docs**: `README.md`, `CONTRIBUTING.md`, `CLAUDE.md` updated for the above.

## Verification / evidence

All on the **working tree** at base `2fb7057`, not yet on a clean checkout of a commit (the
changes were uncommitted when this was written):

- `scripts/checks.sh all` on Python 3.13.18: exit 0. ruff clean; 67 passed; coverage 97.12%
  (`validate_manifests.py` 86% → 100%); example 29 passed at 100%; manifests and eval cases
  valid; shellcheck 0.11.0 clean; `claude plugin validate .` (CLI 2.1.322) passed with two
  warnings (no plugin icon; `CLAUDE.md` at the plugin root is not loaded as context);
  generated app: ruff clean, 3 passed, 3 skipped.
- `scripts/checks.sh quality` and `scaffold` on Python 3.11.18 and 3.12.3: same results.
- New tests were written first and seen to fail (9 scaffold, 3 validator, 3 CI-layout). The
  validator tests that passed on first run were mutation-checked: seven error branches were
  each replaced with `pass`, and each mutation failed exactly one test.
- Generated app, by hand: `cp .env.example .env` then tests pass; adding `BOGUS=1` to `.env`
  stops the import with `extra_forbidden`.
- `claude plugin validate .` was run with an empty `HOME` and passed, which is the evidence
  that it needs no login in CI.

**Not run:** the GitHub Actions workflow itself; Python 3.14 (not installed here); a
`docker build` of the generated app, so the `.dockerignore` is checked by content, not by
inspecting an image; any skill eval.

## Outstanding / next steps

1. **CI must run** on the pushed branch. The new `npm install -g @anthropic-ai/claude-code`
   step and the 3.14 matrix entry have only been reasoned about, not executed.
2. **Not fixed, needs the maintainer:**
   - *Eval transcripts* (review item 3): still pending. They need a clean session.
   - *`SKILL.md` restructure* (item 10): deferred, see Decisions.
   - *Pinning the companion installs* (item 12): needs a commit of
     `awesome-skills/code-review-skill` chosen by the maintainer; that repository was outside
     this session's access.
   - *Copilot and `${CLAUDE_SKILL_DIR}`* (item 11): a fallback sentence was added to the
     scaffold `SKILL.md` without an eval run; whether Copilot sets the variable is still
     unverified.
3. **Tag after merge:** `claude plugin tag --push` creates `disciplined-delivery--v0.3.0`.
4. The generated `test_health.py` prints a Starlette deprecation warning about `httpx` under
   `TestClient`; it passes, and was left alone.
5. Required status checks, if any are configured: job names are unchanged, but the matrix
   entries `py3.10` are gone and `py3.14` are new.

## References

- Review findings: the conversation that produced this report (twelve numbered items).
- `skills/disciplined-delivery/SKILL.md` § Engineering standards, the rules the scaffolder was
  measured against.

## Change log

- 2026-11-10: created.
