"""Guard the decision records in `docs/adr/`.

Fails when a file cites an ADR that does not exist (by path, by a relative link
between records, or as "ADR NNNN"), when an index row does not parse, when the
index (`docs/adr/README.md`) and the records disagree on links or status, or
when the files an index row lists differ from the files that cite that ADR —
so renaming, renumbering or superseding a record cannot silently break its links.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADR_DIR = REPO / "docs" / "adr"
INDEX = ADR_DIR / "README.md"
PATH_CITATION = re.compile(r"adr/(\d{4}-[\w.-]+?\.md)")
SIBLING_LINK = re.compile(r"\]\((?:\./)?(\d{4}-[\w.-]+?\.md)\)")  # only inside docs/adr/
ID_CITATION = re.compile(r"\bADR (\d{4})\b")
TABLE_ROW = re.compile(r"^\| \[.*$", re.MULTILINE)
INDEX_ROW = re.compile(r"^\| \[(\d{4})[^\]]*\]\(([^)]+)\) \| (\w+) \| (.*) \|$")
TEXT_SUFFIXES = {".md", ".py", ".json", ".sh", ".yml", ".yaml", ".toml"}


def _text_files() -> list[Path]:
    """Tracked and new files git would commit, so a local `.venv` or build output is skipped."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    paths = (REPO / name for name in out.split("\0") if name)
    return [p for p in paths if p.suffix in TEXT_SUFFIXES and p.is_file()]


def _records() -> dict[str, Path]:
    return {p.name: p for p in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")}


def _rows() -> list[tuple[str, str, str, str]]:
    return [INDEX_ROW.match(line).groups() for line in
            TABLE_ROW.findall(INDEX.read_text(encoding="utf-8")) if INDEX_ROW.match(line)]


def _cites(text: str, number: str) -> bool:
    return f"ADR {number}" in text or re.search(rf"adr/{number}-", text) is not None


def test_every_cited_adr_exists():
    records = _records()
    numbers = {name[:4] for name in records}
    dangling = []
    for path in _text_files():
        text = path.read_text(encoding="utf-8")
        where = path.relative_to(REPO)
        names = PATH_CITATION.findall(text)
        if path.parent == ADR_DIR:
            names += SIBLING_LINK.findall(text)
        dangling += [f"{where} cites {n}" for n in names if n not in records]
        dangling += [f"{where} cites ADR {n}" for n in ID_CITATION.findall(text)
                     if n not in numbers]
    assert not dangling, dangling


def test_every_index_row_parses():
    rows = TABLE_ROW.findall(INDEX.read_text(encoding="utf-8"))
    assert rows, "docs/adr/README.md has no index rows"
    bad = [row for row in rows if not INDEX_ROW.match(row)]
    assert not bad, f"rows not in '| [NNNN …](file.md) | status | `files` |' form: {bad}"


def test_index_lists_every_adr_with_a_working_link():
    linked = {link for _, link, _, _ in _rows()}
    records = set(_records())
    assert linked == records, f"index links {sorted(linked)}, records {sorted(records)}"


def test_index_status_matches_the_record():
    records = _records()
    wrong = []
    for _, link, status, _ in _rows():
        record = records.get(link)
        text = record.read_text(encoding="utf-8") if record else ""
        match = re.search(r"^status:\s*(\w+)", text, re.MULTILINE)
        if match is None or match.group(1) != status:
            wrong.append(f"{link}: index says {status!r}, record says "
                         f"{match.group(1) if match else None!r}")
    assert not wrong, wrong


def test_index_lists_exactly_the_files_that_cite_each_adr():
    files = [p for p in _text_files() if p.parent != ADR_DIR]
    wrong = []
    for number, _, _, cited_by in _rows():
        listed = set(re.findall(r"`([\w./-]+)`", cited_by))
        citing = {str(p.relative_to(REPO)) for p in files
                  if _cites(p.read_text(encoding="utf-8"), number)}
        if listed != citing:
            wrong.append(f"ADR {number}: listed but not citing {sorted(listed - citing)}, "
                         f"citing but not listed {sorted(citing - listed)}")
    assert not wrong, wrong
