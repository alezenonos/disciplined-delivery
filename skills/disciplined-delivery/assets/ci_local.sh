#!/usr/bin/env bash
# Local CI on a clean checkout. Runs the repository's checks in a temporary worktree of the
# commit at HEAD, never in the working tree, so an untracked file, a stale .venv or a local
# link cannot make a check pass. Optionally tests the commit merged with its base, as the
# host's CI tests a pull request.
#
#   ci_local.sh [--merge-preview] [--base REF] -- <command> [args...]
#
#   --merge-preview  merge REF into the temporary checkout first; a conflict fails (exit 2)
#                    and the command does not run.
#   --base REF       the base to merge (default: origin/main).
#
# Prints the SHA the checks ran on: quote it in the PR body. A check counts only next to the
# commit it covered, and a new commit, a rebase or a moved base needs the checks again. The
# exit status is the command's.
#
# Copy this file into your repository and wrap it with the checks your CI runs, so the two
# cannot drift, e.g. scripts/ci_local.sh:
#   exec "$(dirname "$0")/../vendor/ci_local.sh" "$@" -- sh -c 'ruff check . && pytest -q'
set -euo pipefail

usage() { sed -n '2,/^set -euo/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//' >&2; }

merge_preview=0 base=origin/main
while [ $# -gt 0 ]; do
  case "$1" in
    --merge-preview) merge_preview=1 ;;
    --base) base=${2:?--base needs a ref}; shift ;;
    --) shift; break ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 2 ;;
  esac
  shift
done
if [ $# -eq 0 ]; then echo "usage: a command is required after --" >&2; usage; exit 2; fi

top=$(git rev-parse --show-toplevel)
head_sha=$(git -C "$top" rev-parse HEAD)
short=${head_sha:0:7}

# Untracked files count too: an untracked conftest.py or module changes what the checks see.
if [ -n "$(git -C "$top" status --porcelain)" ]; then
  echo "note: testing commit $short; your uncommitted changes are not tested (commit them first)" >&2
fi

clean=$(mktemp -d)
# shellcheck disable=SC2329  # invoked by the trap below
cleanup() {
  git -C "$top" worktree remove --force "$clean" >/dev/null 2>&1 || rm -rf "$clean"
  git -C "$top" worktree prune >/dev/null 2>&1 || true
}
trap cleanup EXIT
git -C "$top" worktree add -q --detach "$clean" "$head_sha"
tested="a clean checkout of $short"

if [ "$merge_preview" = 1 ]; then
  # Fetch the base first: merging a stale origin/main previews a merge the host will not do.
  # A failed fetch (offline) degrades to the local ref, and says so.
  remote=${base%%/*}
  if [ "$remote" != "$base" ] && git -C "$top" remote | grep -qx "$remote"; then
    git -C "$top" fetch -q "$remote" "${base#*/}" 2>/dev/null ||
      echo "note: could not fetch $base; previewing the merge with the local ref" >&2
  fi
  if ! base_sha=$(git -C "$top" rev-parse -q --verify "$base^{commit}"); then
    echo "local CI for $short: FAIL, base $base is not a commit here; nothing was run"
    exit 2
  fi
  if git -C "$clean" -c user.name=ci-local -c user.email=ci-local@localhost \
       merge -q --no-ff --no-edit "$base_sha" >/dev/null 2>&1; then
    tested="$tested merged with $base ${base_sha:0:7}"
  else
    git -C "$clean" merge --abort >/dev/null 2>&1 || true
    echo "local CI for $short: FAIL, does not merge with $base ${base_sha:0:7}; nothing else was run"
    exit 2
  fi
fi

set +e
(cd "$clean" && "$@")
rc=$?
set -e

if [ "$rc" = 0 ]; then
  echo "local CI for $short: PASS ($tested)"
else
  echo "local CI for $short: FAIL, exit $rc ($tested)"
fi
exit "$rc"
