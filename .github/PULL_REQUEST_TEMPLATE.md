<!--
BEFORE SUBMITTING: Read every word of this template, and CONTRIBUTING.md.
PRs that leave sections blank, contain multiple unrelated changes, or show
no evidence of human involvement will be closed without review.

Adapted from obra/superpowers' PULL_REQUEST_TEMPLATE.md.
-->

> **This PR targets the default branch (`main`).** One branch = one focused
> change; name it `feat/…`, `fix/…`, `chore/…`, `docs/…`, or `test/…`.

## Who is submitting this PR? (required)
<!-- Required. PRs that omit this will be closed. We assume an agent wrote
     this PR — tell us which one and where it ran. We weigh contributions by
     what produced them: content reasoned from documentation is held to a
     different bar than work grounded in a real session. -->

| Field | Value |
|-------|-------|
| Your model + version | |
| Harness + version | |
| All plugins installed | |
| Human partner who reviewed this diff | |

## What problem are you trying to solve?
<!-- Describe the specific problem you encountered. If this was a session
     issue, include: what you were doing, what went wrong, the model's
     exact failure mode, and ideally a transcript or session log.

     "Improving" something is not a problem statement. What broke? What
     failed? What was the user experience that motivated this? -->

## What does this PR change?
<!-- 1-3 sentences. What, not why — the "why" belongs above. -->

## Is this change appropriate for this plugin?
<!-- This plugin ships the `disciplined-delivery` and `scaffold-agentic-app`
     skills and their packaging. Ask yourself:

     - Would this be useful to others who install this plugin, on a
       different kind of project than yours?
     - Is this project-specific, team-specific, or tool-specific?
     - Does this integrate or promote a third-party service?

     If your change is a new skill for a specific domain, workflow tool, or
     third-party integration, it belongs in its own plugin — not here. -->

## What alternatives did you consider?
<!-- What other approaches did you try or evaluate before landing on this
     one? Why were they worse? If you didn't consider alternatives, say so
     — but know that's a red flag. -->

## Does this PR contain multiple unrelated changes?
<!-- If yes: stop. Split it into separate PRs. Bundled PRs will be closed.
     If you believe the changes are related, explain the dependency. -->

## Existing PRs
- [ ] I have reviewed all open AND closed PRs for duplicates or prior art
- Related PRs: <!-- #number, #number, or "none found" -->

<!-- If a related closed PR exists, explain what's different about your
     approach and why it should succeed where the other didn't. -->

## Environment tested

| Harness (e.g. Claude Code, Cursor) | Harness version | Model | Model version/ID |
|-------------------------------------|-----------------|-------|------------------|
|                                     |                 |       |                  |

## New or changed skill (required if this PR adds or edits a skill)

<!-- If this PR adds a new skill or changes an existing one's wording, you
     MUST include a session transcript proving the skill auto-triggers at
     the right moment. A skill that never loads is dead weight — present on
     disk but never invoked.

     ACCEPTANCE TEST: Open a clean session and send a user message that
     should trigger the skill, e.g.:

         disciplined-delivery   -> "Implement <small feature> in this repo"
         scaffold-agentic-app   -> "Scaffold a new agentic/RAG app"

     A working skill auto-triggers (loads without being named explicitly).
     Paste the complete transcript below. See evals/README.md for the
     procedure and evals/cases/<skill>.json for the prompts to run.

     These do NOT count and PRs that rely on them will be closed:

     - Manually invoking the skill by name when the test should auto-trigger it
     - Anything that requires the user to opt in per-session
     - Anything where the skill does not auto-trigger on a representative prompt
-->

<details>
<summary>Clean-session transcript showing the skill auto-triggering</summary>

```
paste the complete transcript here
```

</details>

## Evaluation
- What was the initial prompt you (or your human partner) used to start
  the session that led to this change?
- How many eval sessions did you run AFTER making the change?
- How did outcomes change compared to before the change?

<!-- "It works" is not evaluation. Describe the before/after difference
     you observed across multiple sessions. -->

## Rigor

- [ ] If this is a skills change: I used `superpowers:writing-skills` and
      completed adversarial pressure testing (paste results below)
- [ ] This change was tested adversarially, not just on the happy path
- [ ] I did not modify carefully-tuned behavior-shaping content (the loop
      steps, Red flags list, "stop and ask" gate) without evals showing the
      change is an improvement

<!-- If you changed wording in skills that shape agent behavior, show your
     eval methodology and results. These are not prose — they are code. -->

## Human review
- [ ] A human has reviewed the COMPLETE proposed diff before submission

<!--
STOP. If the checkbox above is not checked, do not submit this PR.

PRs will be closed without review if they:
- Show no evidence of human involvement
- Contain multiple unrelated changes
- Promote or integrate third-party services or tools
- Submit project-specific or personal configuration as plugin changes
- Leave required sections blank or use placeholder text
- Modify behavior-shaping content without eval evidence
-->
