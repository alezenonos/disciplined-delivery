"""Guard the decision records in `docs/adr/`.

Fails when a file cites an ADR that does not exist, when an ADR is missing from
the index (`docs/adr/README.md`), or when the index names a path that does not
exist — so renaming or renumbering a record cannot silently break its links.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADR_DIR = REPO / "docs" / "adr"
INDEX = ADR_DIR / "README.md"
CITATION = re.compile(r"adr/(\d{4}-[\w.-]+?\.md)")
TEXT_SUFFIXES = {".md", ".py", ".json", ".sh", ".yml", ".yaml", ".toml"}


def _text_files():
    for path in REPO.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            yield path


def _records() -> set[str]:
    return {p.name for p in ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md")}


def test_every_cited_adr_exists():
    records = _records()
    dangling = [
        f"{path.relative_to(REPO)} cites adr/{name}"
        for path in _text_files()
        for name in CITATION.findall(path.read_text(encoding="utf-8"))
        if name not in records
    ]
    assert not dangling, dangling


def test_every_adr_is_in_the_index():
    index = INDEX.read_text(encoding="utf-8")
    missing = sorted(name for name in _records() if f"]({name})" not in index)
    assert not missing, f"not in docs/adr/README.md: {missing}"


def test_index_names_only_existing_paths():
    index = INDEX.read_text(encoding="utf-8")
    carried = [p for row in re.findall(r"^\|.*$", index, re.MULTILINE)
               for p in re.findall(r"`([\w./-]+)`", row)]
    assert carried, "the index names no code paths"
    missing = [p for p in carried if not (REPO / p).exists()]
    assert not missing, f"docs/adr/README.md names missing paths: {missing}"
