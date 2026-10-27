#!/usr/bin/env bash
# This repository's local CI: every step of .github/workflows/ci.yml (one Python version, not
# the matrix), on a clean checkout of the commit at HEAD (never the working tree), through the
# runner the plugin ships.
#
#   scripts/ci_local.sh [--merge-preview]     # --merge-preview tests the commit merged with origin/main
#
# Needs ruff, pytest, pytest-cov and the shellcheck binary; one way to get all four is
# `pip install ruff pytest pytest-cov shellcheck-py`. pytest runs as `python3 -m pytest` so the plugin and the interpreter cannot
# differ: on its first clean-checkout run a bare `pytest` resolved to a standalone install
# without pytest-cov and failed (exit 4). The scaffolded app's tests run in a throwaway
# virtualenv, so its requirements never touch your environment; that step needs the network.
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC2016  # single quotes on purpose: the script expands inside the clean checkout
exec skills/disciplined-delivery/assets/ci_local.sh "$@" -- sh -c '
  set -e
  scratch=$(mktemp -d); trap "rm -rf \"$scratch\"" EXIT
  ruff check .
  COVERAGE_PROCESS_START="$PWD/pyproject.toml" python3 -m pytest -q --cov --cov-report=term-missing
  (cd examples/roman-numerals &&
   python3 -m pytest -q --cov=roman --cov=cli --cov-report=term-missing --cov-fail-under=100)
  python3 scripts/validate_manifests.py
  python3 scripts/check_evals.py
  shellcheck install.sh scripts/ci_local.sh skills/disciplined-delivery/assets/ci_local.sh
  python3 skills/scaffold-agentic-app/scaffold.py "$scratch/app" >/dev/null
  python3 -m compileall -q "$scratch/app"
  python3 skills/scaffold-agentic-app/scaffold.py "$scratch/app" | grep -q "created: 0 file(s)"
  python3 -m venv "$scratch/venv"
  "$scratch/venv/bin/pip" install -q -r "$scratch/app/requirements.txt"
  (cd "$scratch/app" && "$scratch/venv/bin/python" -m pytest -q)
'
