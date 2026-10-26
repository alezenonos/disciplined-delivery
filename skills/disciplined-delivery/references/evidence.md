# Evidence, measurement and recording

> The norms behind the "Measurement & rules", "Behaviour-shaping changes" and "Decisions &
> docs" sections of `SKILL.md`. These are not preferences: each was learned from a
> measurement, and each has already reversed a decision its authors were confident about.
> Carry them into the consuming repo's `CLAUDE.md`, each with the report that earned it, and
> cite the report when you follow one.

## 1. Measure before you add a rule or a check

Never ship a prompt rule or an eval check for a failure mode you have not counted in the run
archives. A check for something that occurs zero times is legitimate, but it must say
**"regression guard"** in its comment and in the report, never be presented as a fix.
Precedent: a formatting rule was built and then dropped at 0 occurrences in 259 runs; a
reconciliation feature was scoped, measured, and found to have nothing to reconcile.

## 2. Two runs, or no claim

A single battery cannot distinguish a regression from sampling variance. Any behavioural
claim about a prompt or rule change needs at least two runs on the same configuration.
Precedent: a product rename looked like 25/26 → 23/26 until a repeat on the *same* code
recovered to 25/26. "Same configuration" is the load-bearing part: a targeted subset is
allowed where a change only narrows behaviour, but two incomparable runs are not evidence.

## 3. Report, never exclude

A number that would flatter by hiding a category is worse than an ugly number. Every failure
cause is printed, including `other`; a count that does not add up to the total is a bug.
A reliability line that omits a category is a report of a different population.

## 4. Degrade, never abort

A broken golden file, an unreachable tracing backend, a coverage upload that cannot connect,
or a failing judge costs that *signal*, never the run. Diagnostics must not be able to fail a
turn, a build, or a paid battery. Precedent: a coverage upload failed a TLS handshake and
turned the test job red twice though every test passed; `fail_ci_if_error: false` covered only
errors the uploader reported, not the action failing to connect, so the step itself had to be
`continue-on-error`.

## 5. Fail fast on config; fail closed on privacy

Unknown or empty config keys are boot errors, not silent defaults. The exception is anything
that governs what leaves the process: a capture setting degrades an unrecognised value to the
safest level, so a typo costs observability and never exports a conversation.

## 6. Policy lives in config, not in code

Domain prose belongs in the domain-rules file, engineering knobs in the engineering config,
per-prompt expectations in the eval cases, what a PR must say in the PR template. If a change
to what the product *says* (or what a PR must contain) requires a code change, the seam is in
the wrong place.

## 7. Never claim an answer is correct

Reports separate what is machine-verified (trajectory, tool choice, hygiene, counts) from what
needs the domain owner's approval (faithfulness), and say so in their own text. Trajectory is
not faithfulness. Do not invent `must_mention` / `must_not_mention` / `tolerance` entries for a
golden: those are the domain owner's words, and authoring them yourself scores you against your
own opinion.

## 8. Evidence artefacts are immutable

Never overwrite a committed run; re-render to a new name. A number is quotable only next to
the configuration that produced it (the run stamp, the pinned model and routing). A derived
number, one computed *from* those runs by a script, carries the command that produced it,
with its filter criteria, beside the figure in the document. Precedent: nine review findings
across four documentation PRs in one week, all the same shape: a number or behaviour restated
from a description of the evidence rather than recomputed from it. None was caught by
self-review; the command had existed each time and been thrown away in favour of prose.

## 9. Write the report even when the answer is "no"

A measured negative is a deliverable. Several reports exist solely to record that an idea was
tested and declined, and one records that its author's own objection was wrong. A change that
failed to justify itself is worth more written down than deleted.

## 10. Test what ships, the way its recipient gets it

A check counts only if it ran on a clean checkout of the exact commit (`assets/ci_local.sh`;
`--merge-preview` tests the merge with the base), exercised the real thing rather than a
description of it, and named the SHA it covers. A handoff needs no command from its
recipient: the software sets itself up, or stops at once with a message that needs no
terminal. A setup note is a courtesy, never the fix. See `gates.md` §9.

## 11. Recording

- **Corrections stay visible.** Wrong conclusions are marked `[corrected]` in place, with the
  reasoning error named, rather than silently rewritten. The reasoning error is more reusable
  than the fix.
- **PR bodies carry the known limits**, not only the wins: a confounded baseline, a gap left
  open, a rejected alternative and why.
- **Commit messages explain the decision**, not the diff.
- **Rationale has one home, and the code carries a pointer to it.** Three kinds of knowledge,
  three homes: a *decision* goes in an ADR; a *measurement* in a dated report; what is *locally
  non-obvious* about the code (an invariant, a trap, why a line is the shape it is) stays in the
  comment beside it, in one line that states the invariant and points at the record
  (`# Bounds the FINAL encoded message, not the body: docs/reports/2026-09-20-tool-result-cap.md`).
  The pointer is an ADR id or a `docs/…` path; a PR number alone resolves only on the host and
  says nothing on its own. A module opens with a docstring naming its purpose, its invariants
  and the records that shaped it (code → record); a decision index carries the reverse link
  and each ADR's live status (record → code), and a guard test fails when code cites a record
  that does not exist or the index names code that does not. A decision changes by a dated
  addendum or a new record, never by rewriting the old one. Migrate on touch, not in a sweep.
- **Status lives in the ADR first, the index second.** An index that falls behind two
  acceptances is an index nobody trusts.
- **Every production change is recorded**, by a PR, with what changed, why, how it was tested,
  who made it, and how to undo it. A healthy health endpoint does not prove an answer: after
  the change, someone uses the product and writes down what happened. Secrets are named, never
  shown.

## 12. External writes need explicit approval, and must stand on their own

Tracker task creation and moves, PR comments, and anything posted outside the repo require the
human's say-so first; reading is always fine. The failure mode is quiet: an unsanctioned task
looks identical to a sanctioned one a week later. Messages to a partner are the human's alone;
draft replies go in a file for them to send.

**The tracker is the same channel, not a private one.** A task or comment may *record* that a
question is owed; it must never ask it. The partner reads the board, so a question posted
there is a question sent, which takes the timing and the wording out of the human's hands.

**Anything written to a shared tracker must stand on its own** for someone who was not in the
conversation, including the partner who does not work in this repo. Shorthand does not survive
the trip:

| Not on the board | Write instead |
|---|---|
| a run stamp (`r61`) | what that run **was**: "the 11 September run against the new backend" |
| a config digest | "the model and routing settings we test against", noting what the digest does and does not identify |
| "norm 2" | "our rule that a behavioural claim needs at least two runs on the same configuration" |
| an internal field name | what the check asks, in words |
| `file.py:921` | what the file does, or leave it out |

Quote people verbatim, with the date, when recording their answers: tidied words have twice
been unplaceable by their own author. A task only its author can read costs more than no task,
because it claims the work is captured.

## 13. What CI minutes buy

Measure what each CI job costs and what it caught before cutting or adding one. On the project
this was learned from, the image job was 44% of minutes and caught one real defect; the PR
template check was 14% and caught six; re-running the template check on every push was 37% of
its runs and could catch nothing, since a push cannot change the PR body. **Never skip CI by
path filter:** a workflow-level filter judges a renamed file by its new path, so moving a
prompt's markdown into a "prose" folder would skip CI on the very change that breaks the base.
A regression-guard test keeps CI running on every change.
