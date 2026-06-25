# Outstanding-items review + three follow-ups

| | |
|---|---|
| Date | 2026-06-25 |
| Branch | Split into `chore/release-0.2.1` (PR 1) and `test/eval-scaffolds` (PR 2) |
| Status | Reviewed (`code-review-skill`, no blocking findings) and opened as two focused PRs after human go-ahead |

## Why this task

Asked to review the repo for outstanding work and action what's immediately tractable. Reading
all 11 `docs/reports/` entries against live GitHub state (no open PRs, no open issues, **no remote
tags**) and the green local bar (`ruff` / `pytest` / `check_evals` / `validate_manifests` all
pass) surfaced a recurring set of unfinished items. Most are **blocked on the maintainer**, not on
engineering:

- **Eval transcripts** — need a clean Claude Code session; can't be produced honestly from an
  agent session.
- **`v0.2.1` (and `v0.2.0`) release tag** — no tags exist on the remote; the session git proxy
  returns 403 on tag refs (org policy).
- **Community-marketplace submission** — external form tied to the maintainer's account.

The three items below were the ones actually actionable here.

## What was done

1. **Cut release `0.2.1`.** Bumped `plugin.json` `0.2.0 → 0.2.1` and promoted the `[Unreleased]`
   `scaffold-agentic-app` append-behaviour change into `[0.2.1] - 2026-06-25`, with refreshed
   compare links. Patch-level: a backward-compatible refinement to an existing generator, no API
   change. (Tag push remains a maintainer step — see Outstanding.)

2. **Pre-filled eval transcript scaffolds** for both skills under `evals/transcripts/`
   (`*-pending.md`). Rows are copied verbatim from the `cases/*.json` files; result columns are
   left blank and the files carry a "NOT A REAL RUN" banner. This makes the maintainer's
   clean-session run fill-in-the-blanks without fabricating any result. Rename to
   `<skill>-YYYY-MM-DD.md` once run.

3. **Drafted the `allowed-tools` proposal** (this section, below) — **not** merged into either
   `SKILL.md`. Per the repo's own rule, adding `allowed-tools` is a behaviour-shaping skill change
   that needs an eval run to confirm the skill still functions under the restriction; that
   evidence is exactly item 2's clean-session run, so the merge is gated on it.

## `allowed-tools` proposal (review-only; do not merge without an eval run)

`allowed-tools` narrows what a skill may call. The two skills have very different surface area:

- **`scaffold-agentic-app`** is narrow — it shells out to `scaffold.py` and reads/writes files.
  A restriction is low-risk and worth it:

  ```yaml
  allowed-tools: Read, Write, Edit, Bash, Glob
  ```

- **`disciplined-delivery`** drives the *whole* dev loop (plan/brainstorm, TDD, run
  tests+linter, `git`, `code-review-skill`, open a PR) and delegates into other plugins
  (`superpowers`, `grill-with-docs`). A tight allow-list risks breaking that orchestration.
  Recommend **leaving it unrestricted** until an eval proves a given list is sufficient; if one
  is wanted, the floor is roughly:

  ```yaml
  allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Skill
  ```

**Gate:** land these only after the item-2 transcripts show each skill still auto-triggers and
meets its `expectations` *with the restriction applied* — verify in the clean session, don't
assume.

## Verification

- `ruff check .` ✓ · `pytest -q` ✓ (13) · `python scripts/check_evals.py` ✓ (2/2 covered) ·
  `python scripts/validate_manifests.py` ✓ — re-run after these edits.
- `claude plugin validate .` — not run here (CLI auth); CI is the authoritative gate.

## Outstanding / next steps

1. **Review the two PRs and merge.** The work was split per the methodology: PR 1
   (`chore/release-0.2.1`) is the release cut; PR 2 (`test/eval-scaffolds`) is the transcript
   scaffolds + this report + the append-behaviour eval expectation. The `allowed-tools` proposal
   stays review-only here, gated on the eval run (item 3).
2. **Tag the release** from a normal environment once merged: `git tag disciplined-delivery--v0.2.1
   && git push origin disciplined-delivery--v0.2.1` (and backfill `--v0.2.0` if still missing).
3. **Run the eval cases** in a clean session; fill the `*-pending.md` transcripts. This unblocks
   the `allowed-tools` merge above.
4. **Community-marketplace submission** — maintainer-only; the repo is `validate`-clean.

## Change log

- 2026-06-25: created.
- 2026-06-25: ran `code-review-skill` over the diff (no blocking findings); added an
  append-behaviour expectation to `scaffold-agentic-app` evals (covers the 0.2.1 feature); split
  the work into two focused PRs and updated this report's header/outstanding accordingly.
