# The gates: what each caught, and what it costs

> **A description, not a rulebook.** Every gate in `SKILL.md` was added after it caught, or
> failed to catch, something real on a project that used this skill for several months (an
> LLM chat agent with a FastAPI service, a RAG corpus, a container deployment and a partner's
> desktop app). This file records the evidence and the cost, generalised, so a consuming repo
> can judge whether a gate pays for itself there. If one does not, delete it — that is the
> point of writing the cost down. Keep the same file in your own repo
> (`docs/wiki/how-we-work.md` is the convention) and extend it only when a *new* failure earns
> a gate.

## The loop

```
   decision needed? ── yes ──▶  grill  ──▶  planning md ──┐
          │ no                                            │
          │     ┌───────────────────────────────────────◀─┘
          ▼     ▼
        slice ──▶ TDD (red first) ──▶ review gate ──▶ commit ──▶ PR ──▶ review round ──▶ merge
          ▲                                                                  │
          └──────────────────────── findings ──────────────────────────────◀─┘
```

One slice = one reviewable change. The review round is not a formality: in a sample of six
PRs, four were corrected by it, and in three of those the correction changed the design, not
the code.

## 1. TDD red first, and mutation-check anything that passes immediately

Write the test, watch it fail, watch it fail *for the right reason*. When a test passes the
moment it is written, mutate the implementation and confirm that exactly that test fails
while the others still pass. That is a precise kill, and it is what makes the test worth
keeping.

**Cost:** minutes. **What it buys:** usually nothing on the day; it buys the right to trust the
test later. That is a weaker claim than the other gates make, and it is the honest one.

Revert a mutation with an edit, never `git checkout`: it has destroyed uncommitted work.

**The precondition:** a test that has silently stopped asserting passes its mutation too, and
reads as proof. Three cases in one fortnight: a stop test whose outer loop caught the stop
either way; two disconnect tests on a transport that buffers the whole response, so nothing
disconnected; a string-stripper with `re.S` that swallowed the body and left its `used` set
empty. Where a test derives its subject (parses, globs, filters), assert on the derivation:

```python
assert len(used) >= 5, f"extraction looks broken: only found {sorted(used)}"
```

That line is the difference between a test that fails when the code breaks and one that
fails when *it* breaks. Both are needed; only the first is usually written.

## 2. The review gate, including the deployment surface

Review **where it ships**, not only what it does. Three findings in a row were "inert in a
deployment path" rather than logic bugs: a config directory the container did not `COPY`
(`FileNotFoundError` at import in every container, every test green); compose env defaults
that always beat a newly added config knob, with a model slug that had since been delisted;
a domain-rule key present in the yaml but wired nowhere, rendering to nobody with nothing
complaining. That last direction is now guarded by a test that no rule is orphaned from the
prompt.

**Cost:** about ten minutes per slice. **Caught:** inert config, uncopied files, a skippable
make target.

## 3. Behaviour-shaping changes need a live behavioural run

Unit tests can only assert that rule *text* renders. Every defect the behavioural battery
caught was an interaction between rules, invisible to any assertion about content: adding
"X IS A SAMPLE" made the model explain what the sample consists of, which another rule bans
outright. Two prompts failed the leak check; both had passed the prior baseline.

Note the scope: corpus defects of a different kind (a glossary chunk displaced at `k=5`,
license stubs ranking for a definition) were found by a **retrieval measurement**, not the
battery. The two catch different things; neither substitutes for the other.

**Choosing the subset:** a *narrowing* change (a caveat, a prohibition) needs only the prompts
already on that path; a *broadening* one (a fallback, an "also call X when…") can fire
anywhere, so include the classes a targeted subset would exclude. Applying the narrowing
heuristic to a broadening clause is how an unqualified fallback reached review.

**The gate must render somewhere.** It was enforced through the PR template, whose checkbox
read "Prompt / domain-rule change?", so a corpus-only PR could tick n/a and pass a mandatory
template while ignoring it. The checkbox now names the corpus too. A rule whose enforcing
surface does not mention it is the inert-config failure of §2, reintroduced by the document
describing it.

**The release enforces it, for code too.** The release script puts a commit live only after
two battery runs of its prompt, corpus and answer-making code, from a commit with no
uncommitted or untracked files among them. Two PRs had been merged unmeasured before that
check existed: a rule that only people remember is not enforced.

**Cost:** 10 to 50 minutes and cents to a quarter-dollar per run. **Verdict:** worth it every
time; it caught a regression that would otherwise have shipped.

**Compare against a baseline, and say when the baseline is confounded.** One comparison used a
run five days old on a base that had moved; one prompt's change could not be attributed either
way, and the PR said so rather than claiming a win.

## 4. Verify before asserting, including your own claims

Reviewer findings are usually right but are not evidence: check each against the code before
changing anything. In two rounds, all ten held, and knowing that came from checking.

The same applies inward. Claims that were wrong on inspection, in one week:

| Claim | Reality |
|---|---|
| "ingesting the tool docs would pollute retrieval" | half right, and the asserted half was the wrong half: product retrieval improved sharply, and pollution did occur elsewhere |
| "12 of 22 records carry substantive docs" | 6 real, plus 6 stubs of 48 to 69 characters |
| "this capability is absent from our roadmap" | scoped and blocked on another item, in the planning doc |
| "the remaining uncovered lines are all defensive" | four were untested behaviour |

The pattern: **asserting something is unplanned or unmeasured without reading the document
that planned it or running the measurement.** The expensive part of the process is not the
gates; it is re-deriving context a document already holds.

## 5. Measure the question actually being asked

A measurement can be honest and still answer the wrong question. A retrieval assessment
compared the top hit and concluded "unchanged"; at the runtime `k=5` the retrieved *set*
changed on every query. Before reporting a measurement, state what it would take for the
conclusion to be false, and check that the measurement could detect it.

## 6. Check the local convention before arguing about a standard

A coverage gate was argued with on principle, then researched, then partially conceded, and
the convention that resolved it (`# pragma: no cover` on the `__main__` guard) was two files
away in the same package the whole time. When a gate objects, look at how the code already
meeting it does so, first.

## 7. Confirm you are testing what you built

A green result is only as good as the thing it exercised, and the harness can quietly
exercise something else. Three disguises in one week: a **cached page** (the served file was
current, the loaded one was not; one step from filing a bug against working code); a
**transport that does not transport** (a test client that buffers the whole response, so two
"disconnect mid-turn" tests would pass with or without the change; deleted, not fixed); a
**stale artifact** (a report read after midnight was the previous day's file; the tell was
byte-identical numbers).

The check is cheap and specific: bust the cache, print the version, check the timestamp, or
assert on something only the new code could do. The failure is asymmetric: a stale artifact
usually makes a working change look broken (cheap), but sometimes makes a broken change look
fine (expensive). That asymmetry is why it is a gate, not vigilance.

## 8. A guard is only as good as the paths it reaches

A bound, a stop flag, a cap, a seeded scope: each is written once and then *claimed*
everywhere, and it is the claim that turns out false for one path while the mechanism is
correct. Four times, and every time the mechanism was right:

| The mechanism | The path it did not reach |
|---|---|
| a context seeder | the eval battery never called it: 0 of 1,993 archived runs seeded |
| a stop-aware await | the battery passed `stop_event=None` and *cancelled* instead of stopping |
| a `finally` on a stream | the in-loop stop check returned with the generator suspended, so nothing raised through it |
| racing a tool dispatch against a stop | one tool returned before its first `await`: 0 event-loop iterations during a 0.4 s call |

The enumeration is the work; re-reading the mechanism is not a substitute. Before claiming a
guard holds: `grep` the callers and what each passes (a default of `None` is a path, not an
absence); enumerate the exits, not just the happy one (`grep` the `return`s and terminal
`yield`s); ask what each caller does on **cancellation**, not only on the designed condition.

**`async def` does not mean it suspends.** A coroutine that returns before its first `await`
runs to completion synchronously; racing it against a stop flag is a no-op, and while it runs
every other session stalls. If a coroutine must be interruptible, prove it yields: a heartbeat
task that counts ticks during the call is a two-line test.

**Name the zero point of any bound.** A resume TTL was sized against the turn deadline without
stating that its clock starts when the turn *starts*; at the shipped value the two were equal,
so the terminal event was expired the moment it was written. The first test pinned the
assertion to today's config and passed because `300 == 300`; parametrising past the shipped
value caught the pin, and only review caught that the rule itself was wrong. **Parametrise a
derived bound past its shipped value, and separately state what the bound is measured from.**

**A cap bounds the artefact the operator sees, after all encoding.** A byte cap sliced the
serialised body and serialised the slice again, re-escaping every quote: 1436 bytes against a
1024-byte cap. The bound belongs on the final encoded message, and a cap below its own
envelope is a boot error, not a quiet overshoot.

**Cost:** about fifteen minutes per guard. **Caught:** four false "it holds" claims.

## 9. Test what ships, the way its recipient gets it

A partner's app failed to start on a correct PR: his installed packages predated it, nothing
told him to reinstall, and every check was green because none installed and built his app the
way he does. The same day, local CI passed a PR only because a worktree carried a `.venv` link
a clean clone does not have. Same failure, both sides. The rules that came out of it:

1. **Test a clean checkout of the exact commit, never a working tree.** `assets/ci_local.sh`
   runs every check in a temporary checkout of the commit, so an untracked file or a local
   link cannot make a test pass, and says so when uncommitted edits were not tested.
2. **Test what will merge, not only the branch.** The host tests a PR merged with its base;
   `--merge-preview` does the same, and a conflict fails with nothing else run. Two PRs failed
   only on a bug on the base branch.
3. **Exercise the real thing, not a description of it.** A test that reads source text, or a
   fake standing in for a dependency, cannot fail when the dependency is missing.
4. **Bind the evidence to the commit, and let any change void it.** A local-CI result is a
   status on a SHA; a handoff gate's report names both repositories' SHAs; a release records
   its image tag. A new commit, a rebase or a moved base needs the checks again.
5. **A handoff needs no command from its recipient.** A PR description telling him to run
   `npm ci` did not stop the error happening again; a preflight that installs from the
   lockfile when the packages differ did. The software sets itself up, or stops at once with a
   message that needs no terminal.
6. **"Not checked" is never "passed".** A missing tool, a missing record or a stage that could
   not run is BLOCKED or FAIL, with its reason, in every check you own.
7. **A handoff to another team is ready only after its gate** runs on the exact commit they
   receive (clean install from the lockfile, imports, build, their tests, the upgrade from
   their current install without reinstalling), plus a person's run of the built artefact.
   Its first real run found two gaps in the partner's repo no other check could see.

## 10. Grill first, planning document out

Anything M/L, or anything expensive to undo, goes through a grill before build: questions one
at a time, each with a recommended answer, and anything answerable from the codebase answered
there. One grill resolved nine decisions and found two things no amount of building would
have surfaced early: a recorded assumption of one task invalidated by another, and a detach
that silently broke the Stop button. **Grill tasks together when they share a surface.**

## 11. What this costs

| Gate | Cost | Caught |
|---|---|---|
| TDD + mutation check | minutes per slice | confirmed a test was sound; nothing on the day |
| Review gate / deployment surface | ~10 min per slice | inert config, uncopied files, a skippable target |
| Behavioural run on prompt, rule or corpus changes | 10 to 50 min, cents per run | a quality regression no unit test could see |
| Confirm the artifact under test | seconds | a cached page, a buffering transport, a stale report |
| Verify findings before fixing | ~15 min per round | nothing wasted: every finding held |
| Enumerate a guard's callers and exits | ~15 min per guard | four false "it holds" claims |
| Grill before build | one session per decision cluster | an invalidated assumption, a broken Stop button |
| Clean-checkout local CI, merge preview | seconds per run | a `.venv`-dependent pass; two failures that were the base's |
| Handoff gate on the recipient's exact commit | one run plus a person's try | two gaps in the partner's repo nothing else could see |
| Release refuses an unmeasured prompt | two runs per change to what the model reads | added after two PRs went out unmeasured |
| PR template check in CI | one CI minute per open/edit | six non-compliant descriptions in six weeks |

The expensive part is not the gates. It is re-deriving context that a document already holds.
