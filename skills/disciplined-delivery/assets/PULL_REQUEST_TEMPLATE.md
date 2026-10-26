## What problem does this PR solve?
<!-- The concrete problem or goal. Not "improve X": what was broken or missing? -->

## What does this PR change?
<!-- 1-3 sentences. What, not why. -->

## How was it tested?
<!-- TDD: which tests were added (written red-first) and what each would catch; the pass
     count; the linter; coverage of the changed lines. Name the commit the checks ran on
     (`scripts/ci_local.sh --merge-preview` prints it): a check counts only on a clean
     checkout of the exact commit, and a new commit needs the checks again. Say what was
     NOT run. "Not checked" is never "passed". -->

## Alternatives considered
<!-- Other approaches weighed, and why this one. "None" is a red flag. -->

## Known limits
<!-- What this PR does not cover; a confounded baseline; a finding deferred and why; a
     check that could not run. If a limit is worth knowing at review time it is worth
     writing here. -->

## Single focused change?
- [ ] This PR is one self-contained change (not several unrelated ones)
- Related PRs/issues: <!-- #number, or "none" -->

## Review
- [ ] A human has reviewed the complete diff before merge
- [ ] Behaviour-shaping change (prompt, domain rule, corpus, model, tool spec)? The behavioural
      eval was re-run, at least two runs on the same configuration, and the result is stated
      under "How was it tested?" (n/a otherwise)
- [ ] Ships to a deployment or a recipient (container, package, another team's checkout)? It
      was tested the way its recipient gets it: a clean checkout of the exact commit, the real
      artefact, and the recipient has no command to run after pulling (n/a otherwise)
