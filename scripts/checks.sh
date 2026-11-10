#!/usr/bin/env bash
# This repository's checks, in one place. .github/workflows/ci.yml runs each group as a job
# and scripts/ci_local.sh runs them all on a clean checkout of the commit, so what passes
# locally is what CI checks (tests/test_ci_local.py holds the workflow to that).
#
#   scripts/checks.sh [quality|manifests|scaffold|all]     # default: all
#
# Needs the tools in requirements-dev.txt (`pip install -r requirements-dev.txt`) and, for the
# manifests group, the Claude Code CLI (`npm install -g @anthropic-ai/claude-code`). pytest runs
# as `python3 -m pytest` so the plugin and the interpreter cannot differ: a bare `pytest` once
# resolved to a standalone install without pytest-cov and failed (exit 4). The scaffolded
# app's tests run in a throwaway virtualenv, so its requirements never touch your
# environment; that step needs the network.
set -euo pipefail
cd "$(dirname "$0")/.."

CHECK_GROUPS=(quality manifests scaffold)

usage() { sed -n '2,/^set -euo/p' "$0" | sed '$d' | sed 's/^# \{0,1\}//' >&2; }

quality() {
  ruff check .
  COVERAGE_PROCESS_START="$PWD/pyproject.toml" python3 -m pytest -q --cov --cov-report=term-missing
  (cd examples/roman-numerals &&
   python3 -m pytest -q --cov=roman --cov=cli --cov-report=term-missing --cov-fail-under=100)
}

manifests() {
  python3 scripts/validate_manifests.py
  python3 scripts/check_evals.py
  shellcheck install.sh scripts/ci_local.sh scripts/checks.sh \
    skills/disciplined-delivery/assets/ci_local.sh
  # The authoritative manifest check needs the Claude Code CLI. Without it the group fails:
  # a check that could not run must not end in a PASS that gets quoted in a PR.
  if ! command -v claude >/dev/null 2>&1; then
    echo "FAIL: 'claude plugin validate .' cannot run: the claude CLI is not on PATH." >&2
    echo "      Install it with: npm install -g @anthropic-ai/claude-code" >&2
    return 1
  fi
  claude plugin validate .
}

scaffold() (
  scratch=$(mktemp -d)
  trap 'rm -rf "$scratch"' EXIT
  python3 skills/scaffold-agentic-app/scaffold.py "$scratch/app" >/dev/null
  python3 -m compileall -q "$scratch/app"
  # Re-running must be idempotent: nothing created, nothing overwritten. The output goes to
  # a file first: `scaffold.py | grep -q` under pipefail fails now and then, when grep exits
  # on its match while the generator is still printing (a broken pipe).
  python3 skills/scaffold-agentic-app/scaffold.py "$scratch/app" >"$scratch/rerun.log"
  grep -q "created: 0 file(s)" "$scratch/rerun.log"
  python3 -m venv "$scratch/venv"
  "$scratch/venv/bin/pip" install -q -r "$scratch/app/requirements.txt"
  cd "$scratch/app"
  "$scratch/venv/bin/python" -m pytest -q
)

group=${1:-all}
case "$group" in
  quality|manifests|scaffold) "$group" ;;
  all) for g in "${CHECK_GROUPS[@]}"; do "$g"; done ;;
  -h|--help) usage ;;
  *) echo "unknown group: $group" >&2; usage; exit 2 ;;
esac
