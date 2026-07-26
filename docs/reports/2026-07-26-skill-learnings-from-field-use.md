# Report: Fold field learnings from a downstream project back into `disciplined-delivery`

| | |
|---|---|
| Date created | 2026-07-26 |
| Last edited | 2026-07-26 |
| Author | Claude Opus 5 (Claude Code) |
| Human partner | AZ |
| Status | Blocked — awaiting the live eval session (see Outstanding) |
| Related | branch `docs/skill-field-learnings`; skill `skills/disciplined-delivery/SKILL.md` |

## Task

> "update our skill with all the learnings of ways of working in this project? the idea is for
> this approach to be transferrable. if you see any inconsistencies, gaps, ommissions or rules
> that we shouldnt follow or that we should follow but not captured let's work on it. this should
> be one pr to fix the plugin/skill"

Restated: after several weeks of using this skill on a real agentic-PM project (an LLM chat agent
with a FastAPI service, a RAG corpus, Docker/compose deployment and a partner-owned tool
contract), harvest what the skill *failed to prevent* and what it demanded but nobody did, and fold
both back in so the discipline transfers to the next repo.

## Context

The skill was applied to ~15 merged PRs on the downstream project. It worked: every change was
small, test-first, human-gated. But a pattern emerged in what still went wrong — and it was
consistently **not** the thing the skill was watching.

Three defects in a row reached review despite a green suite and a passing local run, and all three
were "the change is inert or broken where it ships", not "the logic is wrong":

1. A config directory was not `COPY`ed into the container, so the app raised `FileNotFoundError`
   at import in every container deployment while every test passed.
2. A compose file injected env defaults that always beat a newly-added config knob, making the
   knob inert in the documented Docker flow — and the value it injected was a model slug that had
   since been delisted, so the documented `make run` path had been launching against a 404.
3. A third-party SDK's default (`max_retries=2`, which also retries timeouts) sat underneath the
   project's own retry loop, silently tripling worst-case latency versus what the code's own
   comment claimed. Invisible to the suite because every test double replaces the SDK client.

Separately, one work item was queued as "ready to build" purely because an acceptance checklist
had unticked boxes — the code had shipped it weeks earlier. And the skill's own rule that *every*
task produces a `docs/reports/` entry was being quietly ignored for one-line changes.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| How to capture the deployment-path failures | (a) add a red flag; (b) add a dedicated review section; (c) leave to `code-review-skill` | (b) new **"Review the whole surface"** section | Three incidents is a pattern, not a nit. A red flag is too weak to change where attention goes, and `code-review-skill` reviews the diff — it does not know which deployment paths a repo ships. | Agent, approved by AZ |
| Whether to add "read the library's installed source" | (a) skip as too niche; (b) add under review | (b) | The failure mode is invisible to tests *by construction* (fakes replace the client), so no amount of coverage catches it. That is exactly the kind of rule a skill must carry. | Agent, approved by AZ |
| The "every task produces a report" rule | (a) keep; (b) delete; (c) scale to task size | (c) scaled | It was being ignored for XS changes, and an ignored rule erodes the credible ones. A one-line template change does not need a report; a decision-shaped change does. | AZ (raised by agent as a rule we should *stop* following as written) |
| Scope of the ask-before-write gate | (a) git writes only (status quo); (b) all outward-visible actions | (b) | The downstream project needed the same gate for task-tracker posts. The underlying principle was never "git is special" — it is "anything the outside world sees". | Agent, approved by AZ |
| Whether to add an LLM-app-specific section | (a) keep the skill domain-neutral; (b) add a scoped section | (b), clearly scoped | The plugin already ships `scaffold-agentic-app`, so LLM apps are in its remit; prompt/rule changes genuinely are not gated by unit tests, and that needs saying. | Agent, approved by AZ |
| Report for *this* change | (a) none; (b) full report | (b) | Decision-shaped work, so it earns a report under the newly-scoped rule. Dogfooding the rule the same PR introduces. | Agent |

## What was done

- **`skills/disciplined-delivery/SKILL.md`**
  - New loop step **"Establish the ground truth in code"** — grep before building what a doc,
    checklist or ticket claims is missing.
  - New section **"Review the whole surface"** — deployment paths (container `COPY`,
    compose/orchestration env defaults, packaging manifest, CI), third-party defaults read from
    installed source, naming what test doubles cannot cover, escalation triggers, and the
    disclose-don't-silently-self-review rule.
  - New section **"Receiving review findings"** — verify before implementing (references
    `superpowers:receiving-code-review`), fix the cause not the symptom, record deferrals, and
    cite the observation that contradicts your own justification. (An "Evidence honesty" section
    was drafted standalone and **folded in here** after review flagged it as the vaguest,
    least-measurable addition; its "claim only what you ran" bullet already existed in the Verify
    step, and its rot-prone-counts rule moved to the README standard.)
  - New section **"Behaviour-shaping changes (LLM apps)"** — re-run the behavioural eval and state
    the result; prompt in configuration, composed fail-fast; separate domain and engineering lanes.
  - Engineering standards extended: tests that can fail (no constant-vs-literal tautologies; pin
    the wiring, not the value), fail-fast configuration with no dead knobs, rot-prone external
    pins, read-only vendor/partner-owned inputs.
  - Ask-before-write gate widened from git writes to **all outward-visible actions**.
  - Task reports **scaled to task size**, with an explicit XS/S vs M/L rubric so the relaxation
    is not an escape hatch; dated reports named as immutable snapshots; **reconcile the tracker
    and the docs in both directions**.
  - PR-template reference repointed at the consuming repo's template (the relative link resolved
    to this plugin's own copy once installed elsewhere).
  - Red flags extended to match each addition.
- **`evals/cases/disciplined-delivery.json`** — three new triggers (moving a constant into config;
  a checklist claiming a guard is missing; reconciling a board against the docs) and twelve new
  expectations. Review flagged that an earlier round left several new rules unmeasured; the gaps
  called out (vendor-owned inputs, rot-prone pins, contradicting evidence, tracker reconciliation)
  were closed rather than waved through.
- **`CHANGELOG.md`** — Unreleased entries under Added/Changed.
- **Aligned the repo's own statements of the changed rules.** Applying the new
  "review the whole surface" habit to this docs change surfaced four places that would otherwise
  have contradicted the skill they describe:
  - `CLAUDE.md` — "one report per task" / "**Every task leaves a report**" → scaled to
    decision-shaped and M/L work; the ask-before-write gate widened to outward-visible actions.
  - `CONTRIBUTING.md` — the same two rules in the pre-PR checklist and the loop summary.
  - `README.md` — the intro sentence, and the mermaid loop diagram, which still showed a **4-step**
    loop after the skill grew to **6** (new steps 2 "Ground truth in code" and 5 "Review the whole
    surface"); the post-merge report node now reflects the scaled rule.

  This is the finding worth carrying forward: a rule stated in four files is a rule that will rot
  in three of them. The same class of drift the new section warns about in deployment config
  applies verbatim to documentation.

## Verification / evidence

Run locally on this branch, per `CLAUDE.md`'s CI reproduction:

- `ruff check . && pytest -q` — see PR body for the exact counts.
- `python scripts/validate_manifests.py` — manifests + install consistency.
- `python scripts/check_evals.py` — eval cases well-formed; every skill covered.
- `claude plugin validate .` — authoritative manifest check.

No code paths changed: this PR edits skill prose, one eval-case data file, the changelog and this
report. The scaffolder and scripts are untouched, so their behaviour is unchanged.

**Not verified:** the skill's *behavioural* effect. Per the repo's own "skills are code, not prose"
rule, wording that shapes behaviour warrants adversarial testing via `superpowers:writing-skills`.
The eval case here encodes the new expectations as data (the hermetic gate), but the cases are
executed manually against a live session — see `evals/README.md`. That execution has **not** been
run for these new expectations and is the main outstanding item below.

## Outstanding / next steps

- **Run the eval cases against a live session — this PR is gated on it.** The repo's PR template
  requires evals for changes to "the loop steps, Red flags list, 'stop and ask' gate", and this
  change touches **all three**. `evals/README.md` requires a *clean* Claude Code session to test
  auto-triggering and adversarial pushback, which cannot be done from inside the authoring
  session — so it is owed by the human or a fresh session before merge, not skippable here.
  Run it for the new expectations, especially the ones most
  likely to be ignored under time pressure: reviewing the deployment surface, and disclosing a
  missing independent review. Capture the transcript under `evals/transcripts/`.
- **Consider a version bump.** These are additive behaviour-shaping changes to a shipped skill;
  `0.3.0` fits SemVer better than a patch. Left to the human — the release process is theirs.
- **Watch for bloat.** SKILL.md grew from 79 to 120 lines. Every line added here traces to a real
  incident, but a skill that is too long stops being read. If it grows again, consider splitting
  the review discipline into a companion reference file rather than extending inline.
- One learning was deliberately **not** added, as too project-specific to transfer: the exact
  PR-body template wording. (Tracker reconciliation *was* added, in generalised form — "reconcile
  the tracker and the docs in both directions" — after review pointed out that this section and
  the diff disagreed.)

## References

- Downstream project incidents: container `COPY` omission; compose env defaults + delisted model
  slug; SDK `max_retries` compounding; checklist-vs-code divergence.
- `superpowers:receiving-code-review`, `superpowers:writing-skills`.
- `evals/README.md` — how eval cases are executed.

## Change log

- 2026-07-26: created.
