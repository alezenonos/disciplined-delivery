#!/usr/bin/env bash
# This repository's local CI: the checks .github/workflows/ci.yml runs, on a clean checkout of
# the commit at HEAD (never the working tree), through the runner the plugin ships.
#
#   scripts/ci_local.sh [--merge-preview]     # --merge-preview tests the commit merged with origin/main
#
# The coverage gate needs pytest-cov; `pip install ruff pytest pytest-cov` first.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
# shellcheck disable=SC2016  # single quotes on purpose: the script expands inside the clean checkout
exec "$here/../skills/disciplined-delivery/assets/ci_local.sh" "$@" -- sh -c '
  ruff check . &&
  COVERAGE_PROCESS_START="$PWD/pyproject.toml" pytest -q --cov --cov-report=term-missing &&
  python3 scripts/validate_manifests.py &&
  python3 scripts/check_evals.py &&
  python3 skills/scaffold-agentic-app/scaffold.py "$(mktemp -d)/app" >/dev/null
'
