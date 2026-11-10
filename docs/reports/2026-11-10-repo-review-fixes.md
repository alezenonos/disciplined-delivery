# Report: repo review, the fixes that followed, and release 0.3.0

| | |
|---|---|
| Date created | 2026-11-10 |
| Last edited | 2026-11-10 |
| Author | Claude Code (cloud session) |
| Human partner | alezenonos |
| Status | In progress: five PRs open, checked locally on clean checkouts; none reviewed by a human or merged |
| Related | PRs #34 (scaffolder), #35 (validator), #36 (CI checks), #37 (eval negatives), and the release PR that carries this report |

## Task

"Review the repo and suggest improvements", then "Can you fix them all?", then "Do them as
separate PRs. Pin it. Use the latest version." The review listed twelve items. This report
records which were fixed, where, which were not, and why.

## Context

At `2fb7057` the repo was green (ruff clean, 47 tests, 91.5% coverage, manifests valid). The
review's findings were about gaps between what the repo says and what it does: the
scaffolder generated an app that broke the sibling skill's standards, the checks existed in
two hand-kept copies, nothing had been released since 0.2.2, and the validator's failure
branches were untested.

The fixes were first made on one branch and pushed. The human partner then asked for separate
PRs, so each concern was rebuilt on its own branch from `main`. Before the split an
independent review of the combined diff reported ten findings; nine were about the code and
were fixed on the branch they belonged to, and the tenth was the bundling itself.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| One PR or several | one branch with a commit per concern; one PR per concern | one PR per concern | The repo's rule: no bundled changes in one PR. | human |
| Make the PRs independent or stacked | stack #36 on #34; cut the dependency | independent, all based on `main` | The skill says to avoid stacked PRs. The one dependency (linting the generated app from the shared checks script) was dropped from #36 and noted there as a follow-up. | agent |
| How to stop CI and local CI drifting (#36) | a test comparing the two command lists; one script both call | one script, `scripts/checks.sh`, one group per CI job | The lists differed in spelling, so a comparison would be fuzzy. Job names and the matrix shape are unchanged. | agent |
| Claude Code CLI in CI: pin or latest (#36) | latest, unpinned; pinned | pinned to 2.1.322, the latest on 2026-11-10 | The agent first chose unpinned ("what users install with"); the human partner chose a pin. Dependabot cannot see the pin, so the release steps say to check it. | human |
| A missing CLI locally (#36) | report BLOCKED and continue; fail | fail | With BLOCKED the run still ended in PASS, a SHA someone would quote. | agent, after review |
| Generated CI: action pins go stale in `scaffold.py` (#34) | leave `@v4`; pin and cross-check against this repo; pin and generate a `dependabot.yml` | pin and generate | An old SHA still works and the generated repo's Dependabot bumps it. A cross-check would turn every Dependabot PR here red. | agent |
| Model default in the generated app (#34) | two places; one | `app/config.py` only; id updated to `claude-opus-5-5` | "A value in more than one place rots." | agent |
| `extra="forbid"` in generated settings (#34) | forbid alone; forbid and declare the offered keys | declare them | With forbid alone, `cp .env.example .env` stopped the app. | agent |
| Version for the release | 0.2.3; 0.3.0 | 0.3.0 | The unreleased section adds shipped assets and many skill gates: features, not patches. | agent; the human partner did not object when asked |
| Restructure `SKILL.md` (review item 10) | do it now; defer | deferred | It changes what the agent always has in context. The repo's rule requires eval evidence for that, and no eval has been run. | agent |

## What was done

- **#34, scaffolder** (`4d6cc86`): `.dockerignore`; settings that reject an unknown key in the
  `.env` file; one home for the model default; generated CI with pinned actions, a pinned
  `ruff` and `dependabot.yml`; a docstring on every stub; two generated tests that run; one
  project name in three places, taken from the target directory; `app/Dockerfile` removed.
- **#35, validator** (`e769f9f`): frontmatter read as top-level keys; `name` must be non-empty
  and equal the skill's directory; `plugin.json`'s version must have a `CHANGELOG.md` heading;
  a test for every error branch.
- **#36, CI** (`288f663`): `scripts/checks.sh` called by CI and by `scripts/ci_local.sh`;
  `requirements-dev.txt` with pinned tools and a `pip` Dependabot entry; `claude plugin
  validate .` in the checks with the CLI pinned; matrix moved to Python 3.11–3.14.
- **#37, evals** (`d3f3070`): six more negative prompts for `disciplined-delivery`, mirrored
  in the pending transcript.
- **Release PR**: `[Unreleased]` becomes `[0.3.0] - 2026-11-10`; `plugin.json` is bumped to
  `0.3.0`; this report.

## Verification / evidence

Each branch was checked with `scripts/ci_local.sh --merge-preview` (a clean checkout of the
commit merged with `origin/main` `2fb7057`), on Python 3.13.18:

| PR | Commit | Result | Tests | Coverage |
|----|--------|--------|-------|----------|
| #34 | `4d6cc86` | PASS | 58 | 91.69% |
| #35 | `e769f9f` | PASS | 60 | 97.15% |
| #36 | `288f663` | PASS | 52 | 91.50% |
| #37 | `d3f3070` | PASS | 47 | 91.50% |

- The four branches were merged together locally and `scripts/checks.sh all` passed on the
  result: 76 tests, coverage 97.21%, `claude plugin validate .` passed with two warnings (no
  plugin icon; `CLAUDE.md` at the plugin root is not loaded as context), generated app 3
  passed and 3 skipped.
- New-behaviour tests were written first and seen to fail. Validator tests that passed on
  first run were mutation-checked: eleven error branches were each replaced with `pass`, and
  each mutation failed the test written for it.
- The broken-pipe fix in #36 was run 60 times unbuffered with no failure; the reviewer had seen
  1 in 40 before it.
- An earlier revision of #34 and #36 also passed on Python 3.11.18 and 3.12.3.

**Not run:** GitHub Actions on any of the five PRs at the time of writing; Python 3.14 (not
installed in the session); a `docker build` of the generated app; any skill eval.

## Outstanding / next steps

1. **Human review of all five PRs.** None has been reviewed; each says so.
2. **Merge order: this release PR last.** Merged earlier, it would release 0.3.0 without the
   fixes. #34–#37 are independent of each other and merge cleanly in any order. #36 and the
   open Dependabot PR #33 edit the same lines of `ci.yml`; the second to merge needs a rebase.
3. **Tag after the release PR merges:** `claude plugin tag --push` creates
   `disciplined-delivery--v0.3.0`.
4. **Not fixed, needs the maintainer:**
   - *Eval transcripts* (item 3): still pending. They need a clean session.
   - *`SKILL.md` restructure* (item 10): deferred, see Decisions.
   - *Pinning the companion installs* (item 12): needs a commit of
     `awesome-skills/code-review-skill` chosen by the maintainer; that repository was outside
     this session's access.
   - *Copilot and `${CLAUDE_SKILL_DIR}`* (item 11): #34 adds a fallback sentence to the scaffold
     `SKILL.md` without an eval run. Whether Copilot sets the variable is unverified.
5. **Follow-up once #34 and #36 are both merged:** lint the generated app from
   `scripts/checks.sh scaffold` with the app's own pinned ruff.
6. `claude plugin validate` warns that the plugin has no icon. Not addressed.
7. The first, bundled branch (`ccr-94f8b1bc-vmo0co`) is superseded by the five PRs and can be
   deleted.

## References

- PRs #34, #35, #36, #37 and the release PR.
- `skills/disciplined-delivery/SKILL.md` § Engineering standards, the rules the scaffolder was
  measured against.

## Change log

- 2026-11-10: created.
