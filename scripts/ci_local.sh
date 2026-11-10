#!/usr/bin/env bash
# This repository's local CI: every check .github/workflows/ci.yml runs (one Python version,
# not the matrix), on a clean checkout of the commit at HEAD (never the working tree), through
# the runner the plugin ships.
#
#   scripts/ci_local.sh [--merge-preview]     # --merge-preview tests the commit merged with origin/main
#
# The checks themselves live in scripts/checks.sh, which CI calls too, so the two cannot
# drift. Needs the tools in requirements-dev.txt: `pip install -r requirements-dev.txt`.
set -euo pipefail
cd "$(dirname "$0")/.."
exec skills/disciplined-delivery/assets/ci_local.sh "$@" -- scripts/checks.sh
