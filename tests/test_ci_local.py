"""Tests for the shipped clean-checkout CI runner (`assets/ci_local.sh`).

A throwaway git repository stands in for the checkout. The runner must execute the
checks in a temporary checkout of the commit, never the working tree, and must test the
commit merged with its base when asked.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
ASSET = REPO / "skills" / "disciplined-delivery" / "assets" / "ci_local.sh"
WRAPPER = REPO / "scripts" / "ci_local.sh"

GIT_ENV = {
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
}


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True,
                   env={**os.environ, **GIT_ENV})


def commit_file(repo: Path, rel: str, text: str = "changed\n") -> None:
    path = repo / rel
    path.write_text(text, encoding="utf-8")
    git(repo, "add", rel)
    git(repo, "commit", "-qm", f"edit {rel}")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repo whose origin/main is its first commit, checked out on a feature branch."""
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    (r / "README.md").write_text("base\n", encoding="utf-8")
    git(r, "add", ".")
    git(r, "commit", "-qm", "base")
    git(r, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(r, "checkout", "-qb", "feat/x")
    return r


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(ASSET), *args], cwd=repo, capture_output=True, text=True,
                          env={**os.environ, **GIT_ENV})


def head(repo: Path) -> str:
    return subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()


def test_the_asset_is_executable() -> None:
    assert os.access(ASSET, os.X_OK)


def test_runs_the_checks_in_a_clean_checkout_not_the_working_tree(repo: Path) -> None:
    # An untracked file (a stale .venv link, a local conftest) must be invisible to the checks.
    (repo / "extra.txt").write_text("untracked\n", encoding="utf-8")
    out = run(repo, "--", "sh", "-c", "test ! -e extra.txt && test -e README.md")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "not tested" in out.stderr, "it says when uncommitted changes were not tested"


def test_names_the_commit_and_propagates_the_exit_status(repo: Path) -> None:
    out = run(repo, "--", "sh", "-c", "exit 3")
    assert out.returncode == 3
    assert f"local CI for {head(repo)}" in out.stdout
    assert "FAIL" in out.stdout
    ok = run(repo, "--", "true")
    assert ok.returncode == 0 and "PASS" in ok.stdout


def test_merge_preview_tests_the_commit_merged_with_its_base(repo: Path) -> None:
    # main gains a file after the branch forked; only the merged tree has it.
    commit_file(repo, "feature.txt")
    git(repo, "checkout", "-q", "main")
    commit_file(repo, "on-main.txt")
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(repo, "checkout", "-q", "feat/x")

    plain = run(repo, "--", "test", "-e", "on-main.txt")
    assert plain.returncode == 1
    merged = run(repo, "--merge-preview", "--", "test", "-e", "on-main.txt")
    assert merged.returncode == 0, merged.stderr
    assert "merged with origin/main" in merged.stdout


def test_merge_preview_fails_on_a_conflict_and_runs_nothing(repo: Path, tmp_path: Path) -> None:
    commit_file(repo, "README.md", "branch\n")
    git(repo, "checkout", "-q", "main")
    commit_file(repo, "README.md", "main\n")
    git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    git(repo, "checkout", "-q", "feat/x")

    marker = tmp_path / "ran"
    out = run(repo, "--merge-preview", "--", "touch", str(marker))
    assert out.returncode == 2
    assert "does not merge" in out.stdout
    assert not marker.exists(), "nothing runs on a tree that does not merge"


def test_merge_preview_with_an_unknown_base_fails_with_a_summary(repo: Path) -> None:
    out = run(repo, "--merge-preview", "--base", "no/such-ref", "--", "true")
    assert out.returncode == 2
    assert f"local CI for {head(repo)}: FAIL" in out.stdout
    assert "no/such-ref" in out.stdout


def test_merge_preview_fetches_the_base_first(repo: Path, tmp_path: Path) -> None:
    # A real remote that moved after our last fetch: the preview must see its new commit.
    upstream = tmp_path / "upstream.git"
    git(repo, "clone", "-q", "--bare", str(repo), str(upstream))
    git(repo, "remote", "add", "origin", str(upstream))
    git(repo, "fetch", "-q", "origin")
    pusher = tmp_path / "pusher"
    git(tmp_path, "clone", "-q", "-b", "main", str(upstream), str(pusher))
    commit_file(pusher, "late.txt")
    git(pusher, "push", "-q", "origin", "main")

    out = run(repo, "--merge-preview", "--", "test", "-e", "late.txt")
    assert out.returncode == 0, out.stdout + out.stderr


def test_leaves_no_worktree_behind(repo: Path) -> None:
    run(repo, "--", "true")
    listing = subprocess.run(["git", "worktree", "list"], cwd=repo, check=True,
                             capture_output=True, text=True).stdout
    assert len(listing.strip().splitlines()) == 1, listing


def test_a_missing_command_is_a_usage_error(repo: Path) -> None:
    out = run(repo)
    assert out.returncode == 2
    assert "usage" in (out.stdout + out.stderr).lower()


def test_this_repo_wraps_the_asset_with_its_own_checks() -> None:
    # Not run here: the wrapper runs this suite, which would run the wrapper. A smoke check.
    assert os.access(WRAPPER, os.X_OK)
    text = WRAPPER.read_text(encoding="utf-8")
    assert "assets/ci_local.sh" in text
    # Every step of .github/workflows/ci.yml, so a PASS here means what CI's PASS means.
    for check in ("ruff check", "pytest", "examples/roman-numerals", "--cov-fail-under=100",
                  "validate_manifests.py", "check_evals.py", "shellcheck", "compileall",
                  "created: 0 file(s)"):
        assert check in text, check
