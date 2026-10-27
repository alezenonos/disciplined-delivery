# Decision records

One line per ADR: its status, and the files that cite it (record → code). The decisions also
shape the shipped skill (`skills/*/SKILL.md`), which carries no `docs/adr` link because it is
installed into other repos where that path would not resolve.
Status lives in the ADR first; update this line in the same change.
`tests/test_adr_index.py` fails when a tracked file cites an ADR that does not exist (by path
or as "ADR NNNN"), an ADR is missing from this index, a link or status here disagrees with the
record, or a file listed here does not cite its ADR.

| ADR | Status | Carried by |
|-----|--------|------------|
| [0001 — Independent pre-PR review; grilling the agent can start](0001-independent-review-and-agent-runnable-grilling.md) | accepted | `CLAUDE.md`, `CONTRIBUTING.md` |
