# Decision records

One line per ADR: its status, and every file outside `docs/adr/` that git would commit (tracked,
or new and not ignored) and that cites it
(record → code). The decisions also shape the shipped skill (`skills/*/SKILL.md`), which carries no `docs/adr` link because it is
installed into other repos where that path would not resolve.
Status lives in the ADR first; update this line in the same change.
`tests/test_adr_index.py` fails when such a file cites an ADR that does not exist (by path
or as "ADR NNNN"), an ADR is missing from this index, a link or status here disagrees with the
record, or the files listed here differ from the files that cite the ADR.

| ADR | Status | Cited by |
|-----|--------|------------|
| [0001 — Independent pre-PR review; grilling the agent can start](0001-independent-review-and-agent-runnable-grilling.md) | accepted | `CHANGELOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `docs/reports/2026-10-27-independent-review-and-grilling.md` |
