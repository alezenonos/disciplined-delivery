"""Guard the decision records in `docs/adr/`.

Fails when a tracked file cites an ADR that does not exist (by path or as
"ADR NNNN"), when an ADR is missing from the index (`docs/adr/README.md`), when
an index link or status disagrees with the record, or when a file the index
lists does not cite its ADR — so renaming, renumbering or superseding a record
cannot silently break its links.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADR_DIR = REPO / "docs" / "adr"
INDEX = ADR_DIR / "README.md"
PATH_CITATION = re.compile(r"adr/(\d{4}-[\w.-]+?\.md)")
ID_CITATION = re.compile(r"\bADR (\d{4})\b")
INDEX_ROW = re.compile(r"^\| \[(\d{4})[^\]]*\]\(([^)]+)\) \| (\w+) \| (.*) \|$", re.MULTILINE)
TEXT_SUFFIXES = {".md", ".py", ".json", ".sh", ".yml", ".yaml", ".toml"}


def _tracked_text_files() -> list[Path]:
    """Files git tracks, so a local `.venv` or build output is never scanned."""
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout
    paths = (REPO / line for line in out.splitlines())
    return [p for p in paths if p.suffix in TEXT_SUFFIXES and p.is_file()]


def _records() -> dict[str, Path]:
    return {p.name: p for p in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")}


def _rows() -> list[tuple[str, str, str, str]]:
    return INDEX_ROW.findall(INDEX.read_text(encoding="utf-8"))


def test_every_cited_adr_exists():
    records = _records()
    numbers = {name[:4] for name in records}
    dangling = []
    for path in _tracked_text_files():
        text = path.read_text(encoding="utf-8")
        where = path.relative_to(REPO)
        dangling += [f"{where} cites adr/{n}" for n in PATH_CITATION.findall(text)
                     if n not in records]
        dangling += [f"{where} cites ADR {n}" for n in ID_CITATION.findall(text)
                     if n not in numbers]
    assert not dangling, dangling


def test_index_lists_every_adr_with_a_working_link():
    records = _records()
    rows = _rows()
    assert rows, "docs/adr/README.md has no index rows"
    linked = {link for _, link, _, _ in rows}
    assert linked == set(records), f"index links {sorted(linked)}, records {sorted(records)}"


def test_index_status_matches_the_record():
    records = _records()
    wrong = []
    for _, link, status, _ in _rows():
        match = re.search(r"^status:\s*(\w+)", records[link].read_text(encoding="utf-8"),
                          re.MULTILINE)
        if match is None or match.group(1) != status:
            wrong.append(f"{link}: index says {status!r}, record says "
                         f"{match.group(1) if match else None!r}")
    assert not wrong, wrong


def test_each_listed_file_cites_its_adr():
    missing = []
    for number, _, _, carried_by in _rows():
        paths = re.findall(r"`([\w./-]+)`", carried_by)
        assert paths, f"ADR {number} lists no files that cite it"
        for p in paths:
            target = REPO / p
            if not target.is_file() or f"ADR {number}" not in target.read_text(encoding="utf-8"):
                missing.append(f"{p} does not cite ADR {number}")
    assert not missing, missing
