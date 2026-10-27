# Decision records

One line per ADR: its status, and where the decision lives in code and docs (record → code).
Status lives in the ADR first; update this line in the same change.
`tests/test_adr_index.py` fails when a file cites an ADR that does not exist, an ADR is
missing from this index, or this index names a path that does not exist.

| ADR | Status | Carried by |
|-----|--------|------------|
| [0001 — Independent pre-PR review; grilling the agent can start](0001-independent-review-and-agent-runnable-grilling.md) | accepted | `skills/disciplined-delivery/SKILL.md`, `CLAUDE.md`, `CONTRIBUTING.md` |
