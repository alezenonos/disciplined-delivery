# Report: Add `examples/` to the root README layout

| | |
|---|---|
| Date created | 2026-06-25 |
| Last edited | 2026-06-25 |
| Author | Claude Opus 4.8 (Claude Code) |
| Human partner | ale_zenonos@hotmail.com |
| Status | In progress (awaiting CI + human merge) |
| Related | branch `docs/readme-examples-layout`; follows merged PR #19 |

## Task

The human asked whether the README was "up to the standard defined in the plugin." Audit
found the root `README.md` Layout section was stale: PR #19 added a top-level `examples/`
directory but did not list it. The human chose to fix it in a new PR. Goal: bring the root
README back in sync with the actual tree.

## Context

The `disciplined-delivery` skill's engineering standards require the README to describe "the
project layout" and be updated "in the same change that changes behavior." PR #19
(`examples/roman-numerals/`) is merged into `main` but its README layout update was missed,
so this is a follow-up rather than a same-change fix.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Fix now vs. leave | new PR vs. leave stale | New PR | README layout is part of "done" per the plugin standard; the omission is a real (if small) miss | Human |
| Scope | README only vs. broader README audit | README layout line only | Rest of the root README was verified accurate; surgical change, no drive-by edits | Agent |

## What was done

- `README.md` — added an `examples/` entry (with `roman-numerals/`) to the Layout block,
  placed between `evals/` and `scripts/` to match the alphabetical-ish grouping already there.

## Verification / evidence

- `git diff README.md` — single two-line addition, no other changes.
- No code touched, so test/lint behavior is unchanged; `ruff check .` does not lint Markdown.
- Remaining root-README sections re-read and confirmed current (install steps, layout of
  other dirs, development commands).

## Outstanding / next steps

- Awaiting CI green on the branch and human merge of the follow-up PR.

## References

- Merged PR #19 (the example this documents).
- `skills/disciplined-delivery/SKILL.md` — the README standard being met.

## Change log

- 2026-06-25: created; README layout synced with the merged `examples/` directory.
