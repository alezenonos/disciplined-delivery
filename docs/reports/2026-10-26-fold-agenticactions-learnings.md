# Report: Fold the agenticActions ways of working into `disciplined-delivery`

| | |
|---|---|
| Date created | 2026-10-26 |
| Last edited | 2026-10-26 |
| Author | Claude (Claude Code, cloud session) |
| Human partner | AZ |
| Status | Complete on the authoring side; blocked on the live eval session before merge (see Outstanding) |
| Related | branch `ccr-1642c56c-4q2yqv`; skill `skills/disciplined-delivery/SKILL.md`; source repo `alezenonos/agenticActions` |

## Task

> "All of our learnings in terms of how to develop code with minimal logical flaws and bugs in
> steps with best practices and proper templated PRs should be implemented and followed in the
> disciplined delivery plugin. This would allow us to repeat the same project work ethic, ways of
> working and approach to other work we do."

Restated: harvest everything the agenticActions project learned about process since the July
fold-in (`2026-07-26-skill-learnings-from-field-use.md`), both the rules and the mechanisms that
enforce them, and put it into the plugin so the next repo starts with the same discipline and the
same tooling rather than re-learning it.

## Context

The July report folded the first three months of field use into the skill. Since then the
source project added the things that were missing from a skill that was already right about
*what* to do but silent on *how to make it stick*:

- **Ten repository norms** in its `CLAUDE.md`, each tied to the measurement that earned it
  (measure before adding a rule; two runs or no claim; report never exclude; degrade never abort;
  fail fast on config and closed on privacy; policy in config; never claim correct; immutable
  evidence; write the negative report; test what ships the way its recipient gets it).
- **A "how we work" wiki** (`docs/wiki/how-we-work.md`, §2.1–2.9, §3–6) that records each gate
  with the incident that earned it and its cost, and an explicit instruction to delete gates that
  stop paying for themselves.
- **Mechanisms, not reminders**: a PR template enforced by a CI check; a local CI script that
  runs on a clean checkout of the exact commit and can test the merge with `main`; a release
  script that refuses an unmeasured prompt; a handoff gate on the partner's exact commit; a
  check that compares tool specs against the partner's source; a citation guard between code and
  decision records.
- **The October process-tightening review** (`2026-10-13-process-tightening-review.md`), whose
  one-line summary is the thesis of this change: *a rule that only people remember is not
  enforced, and an instruction to a person is not a fix.*

The existing skill had the rules of the loop; it did not have mutation checks, clean-checkout
verification, guard-path enumeration, the measurement norms, or any shipped mechanism. Its PR
template was the obra-derived one for *this* repo (skills are code), not a template a consuming
repo could adopt.

## Decisions

| Decision | Options | Chosen | Why | Decided by |
|----------|---------|--------|-----|------------|
| Where the new material lives | (a) extend `SKILL.md` inline; (b) one line per rule in `SKILL.md`, reasoning in reference files; (c) a second skill | (b) `references/gates.md` + `references/evidence.md` | The July report warned that a skill that is too long stops being read and recommended a companion reference file on the next growth. `SKILL.md` keeps the rule; the reference keeps the incident and the cost, which is what lets a consumer decide to delete a gate. | Agent, following the July report's own recommendation |
| Ship mechanisms or only prose | (a) prose only; (b) ship copyable assets | (b) `assets/`: PR template, checker, workflow, clean-checkout runner | The source project's central October finding: every rule that was only prose was eventually skipped (two unmeasured merges, a `.venv`-dependent pass, a setup note that did not stop the error). "Proper templated PRs" in the task means enforced, not requested. | Agent; the ask names templated PRs explicitly |
| Checker rules hardcoded or read from the template | (a) hardcoded section list as in the source repo, with a test that it matches the template; (b) derived from the template | (b) | Norm 6: policy lives in config. A consuming repo that edits its template must not have to edit Python, and a hardcoded list drifts from the template it describes (the very failure §2.3 records for the checkbox wording). `--must-tick` names a section the template lacks → config error, not silent no-op (norm 5). | Agent |
| Which consumer template | (a) copy this repo's obra-derived template; (b) generalise the source project's lean template | (b), plus a "Known limits" section | The obra template is for a plugin repo where skills are code (transcripts, eval sessions). A product repo needs problem / change / how tested / alternatives / limits / single change / review. "Known limits" comes from how-we-work §4 ("PR bodies carry the known limits"). The two project-specific review boxes became two generic ones (behaviour-shaping; ships to a recipient). | Agent |
| Port `ci_local.sh` whole or the transferable core | (a) port the 300-line script; (b) the clean-checkout + merge-preview core, taking the checks as a command | (b), ~70 lines | The source script's planning (which stage to run per changed path), `--post` (commit status via `gh`) and per-stage parsers are that project's. The transferable rules are §2.9 1, 2 and 4: a clean checkout of the commit, the merge preview, the SHA named. A consuming repo wraps it with its own commands so local CI and hosted CI cannot drift. | Agent |
| Dogfood in this repo | (a) ship only; (b) use the assets here too | (b) `pr-template.yml` on this repo's template, `scripts/ci_local.sh` wrapping the runner | Norm 10: test what ships, the way its recipient gets it. The checker is exercised on two real templates in the tests; the workflow runs it for real on this repo's PRs. | Agent |
| Dependabot PRs and the template check | (a) let them fail the check; (b) skip the job for `dependabot[bot]` | (b) | This repo takes grouped Dependabot PRs (#26); Dependabot writes its own bodies. A check that is red on every bot PR trains people to ignore it. | Agent |
| Test the `pr-template.yml` workflow's triggers | (a) a YAML-parsing test as the source repo has; (b) none | (b) | Norm 1: the source repo's test guards a measured 37% cost. Nothing has been measured here; a test would need PyYAML in CI for a 15-line file. Noted as a regression guard a consumer may add once they measure. | Agent |
| Version bump | (a) bump to 0.3.0 now; (b) leave to the maintainer | (b) | The release process is the maintainer's (`CONTRIBUTING.md`); the July report left the same call. Two additive behaviour-shaping rounds are now under Unreleased, which fits a minor bump. | Agent, deferred to AZ |
| Project-specific learnings deliberately not transferred | | the release script's prompt-digest gate, the partner handoff gate, the merged-panel check, the spec-vs-source check, the production changelog format | They are stated as *standards* in the skill (a release refuses what was not measured; a handoff gate on the exact commit; specs compared against the partner's source by a check; every production change recorded with its rollback) but their code is bound to that project's artefacts. A consumer builds its own from the standard. | Agent |

## What was done

- **`skills/disciplined-delivery/SKILL.md`** — the loop gains mutation checks and the
  "still asserting" precondition (step 3); clean-checkout verification, the artifact-under-test
  check, SHA-bound evidence and BLOCKED-never-passed (step 4); "answer from the codebase" and
  "grill together" (step 1); "check the local convention first" (step 2). New bullets under
  *Review the whole surface* (test what ships the way its recipient gets it; a guard is only as
  good as the paths it reaches), *Receiving review findings* (verify your own claims; repeated
  findings mean root cause), *Branch & PR conventions* (enforced template; known limits; a gate
  must render in an enforcing surface; CI minutes; never a path filter), *Engineering standards*
  (degrade never abort; fail closed on privacy; honest check states; release/deploy as reviewed
  scripts with a logged rollback; specs compared against the partner's source), *Behaviour-shaping
  changes* (corpus and answer-making code in scope; two runs or no claim; narrowing vs broadening;
  confounded baseline; the release refuses unmeasured; never claim correct). New sections
  **Ships with** and **Measurement & rules**. *Decisions & docs* gains rationale-has-one-home,
  visible corrections, the negative report, the living how-we-work, and tracker entries that
  stand on their own. Nine red flags added.
- **`skills/disciplined-delivery/references/gates.md`** — the gates with the incidents that
  earned them and their cost, generalised from how-we-work §1–3 and §6 (no partner, product or
  tracker names).
- **`skills/disciplined-delivery/references/evidence.md`** — norms 1–10, how-we-work §4 and §5,
  and the CI-minutes lesson, generalised.
- **`skills/disciplined-delivery/assets/`** — `PULL_REQUEST_TEMPLATE.md`, `check_pr_template.py`,
  `pr-template.yml`, `ci_local.sh`.
- **This repo dogfoods them** — `.github/workflows/pr-template.yml` (SHA-pinned checkout, runs the
  shipped checker on this repo's template with `--must-tick "Existing PRs"`, skips Dependabot);
  `scripts/ci_local.sh` wrapping the runner with CI's exact commands; "How was it tested?" added to
  this repo's PR template; shellcheck covers the two new scripts; coverage measures the assets.
- **Tests** — `tests/test_check_pr_template.py` (12: compliant / empty / raw template / missing
  section / comment-only section / unticked must-tick / optional checkbox / must-tick config error
  / rules derived from an ad-hoc template / body from file / this repo's own template / the
  consumer template filled) and `tests/test_ci_local.py` (8: executable; clean checkout hides an
  untracked file and warns; SHA and exit status; merge preview sees the base's file; conflict runs
  nothing; no worktree left behind; usage error; this repo's wrapper names CI's checks).
- **Docs in sync** — `CLAUDE.md` (clean-checkout reproduction; the template check),
  `CONTRIBUTING.md`, `README.md` (diagram steps 3–5, layout, development, a new "Adopting it in
  your repo" section), `CHANGELOG.md` (Unreleased).
- **Evals** — `evals/cases/disciplined-delivery.json`: four new triggers (a test that passed at
  once; "CI is off, just run it here"; add a prompt rule; set up template + local CI) and nine new
  or extended expectations; the pending transcript scaffold regenerated from the case file so the
  two cannot disagree.

## Verification / evidence

Run on this branch, on the working tree during development and then on a clean checkout of the
commit through `scripts/ci_local.sh --merge-preview` (the SHA is in the PR body; the report is
written before the final commit exists, so it is not quoted here):

- `ruff check .` — clean.
- `pytest -q --cov` with the coverage gate — 33 passed; coverage above the 85% gate, with the
  new checker measured (see the PR body for the exact figure).
- `python scripts/validate_manifests.py`, `python scripts/check_evals.py` — valid.
- `claude plugin validate .` — passed with the CLI's standing warnings.
- `shellcheck install.sh scripts/ci_local.sh skills/disciplined-delivery/assets/ci_local.sh` —
  clean (two info-level findings annotated with their reason: deliberate single quotes; a
  function invoked by `trap`).
- The scaffold generator self-test (generate, compile, idempotent re-run).
- **Mutation checks** (the gate this change adds, applied to itself): running the checks in the
  working tree instead of the clean checkout failed exactly the two tests about the clean checkout
  and the merge preview; dropping the prose-section rule failed exactly the three tests about
  comment-only sections. Both reverted by edit.

**Not verified:**

- The skill's *behavioural* effect: this change edits the loop steps, the red flags and the
  stop-and-ask surroundings, so per the PR template's Rigor section it needs a clean-session eval
  run. That cannot be done from the authoring session (`evals/README.md`).
- `.github/workflows/pr-template.yml` has not run on GitHub: it fires on a PR being opened or
  edited, which has not happened yet. The checker it calls is tested with this repo's template in
  `tests/test_check_pr_template.py`.
- The consumer assets in a *third* repo. They were exercised on this repo and on throwaway
  repositories in the tests, not on a consumer with its own CI.

## Outstanding / next steps

- **Run the eval cases in a clean session before merge** — the four new triggers and the
  expectations most likely to be skipped under pressure: mutation-checking a first-run pass,
  refusing to call a working-tree green "done", and reporting BLOCKED rather than passed. Save the
  transcript under `evals/transcripts/` and link it from the PR.
- **Open the PR and watch the template check run** for the first time on this repo; if it rejects
  a legitimately filled body, the rule to adjust is in the template, not the checker.
- **Version bump to 0.3.0** is owed by the maintainer; the Unreleased section now holds two rounds
  of additive behaviour-shaping changes.
- **`SKILL.md` grew from 120 to about 160 lines.** The reasoning moved out to references, so the
  per-line density is higher, not lower. If it grows again, the next split is the
  *Engineering standards* section into a reference.
- **The regression guard on the workflow's trigger types** (opened/edited/reopened, no
  `synchronize`) was not added: nothing has been measured here. Add it when a consumer counts the
  cost (the source repo measured 37% of the check's runs as unspendable).
- **Learnings deliberately left project-bound** (see Decisions): a consumer that ships a prompt,
  a partner handoff or a production service builds its own release gate, handoff gate and
  spec-vs-source check from the standards the skill now states.

## References

- `alezenonos/agenticActions`: `CLAUDE.md` (norms 1–10), `docs/wiki/how-we-work.md`,
  `docs/reports/2026-10-13-process-tightening-review.md`, `docs/reports/2026-10-12-ci-minutes.md`,
  `docs/architecture/decisions/README.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `.github/scripts/check_pr_template.py`, `.github/workflows/pr-template.yml`,
  `scripts/ci_local.sh`, `tests/test_pr_template.py`, `tests/test_ci_workflow.py`.
- This repo: `docs/reports/2026-07-26-skill-learnings-from-field-use.md` (the previous fold-in and
  its bloat warning), `evals/README.md`.

## Change log

- 2026-10-26: created.
