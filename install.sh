#!/usr/bin/env bash
#
# Install the disciplined-delivery plugin and its companions.
#
# Installs:
#   - disciplined-delivery + scaffold-agentic-app skills (this plugin)
#   - superpowers (auto-resolved dependency, from obra's marketplace)
# Then prints the one manual step for the grill-me companion skill.
#
# Usage: ./install.sh
set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "error: the 'claude' CLI was not found on PATH." >&2
  echo "Install Claude Code first: https://code.claude.com/docs" >&2
  exit 1
fi

echo "==> Adding obra's superpowers marketplace (dependency source)"
echo "    A dependency from a marketplace you have not added is left unresolved,"
echo "    so this must come before installing the plugin."
claude plugin marketplace add obra/superpowers-marketplace

echo "==> Adding this marketplace"
claude plugin marketplace add alezenonos/disciplined-delivery

echo "==> Installing disciplined-delivery (auto-resolves the superpowers dependency)"
claude plugin install disciplined-delivery@alezenonos

cat <<'EOF'

==> Done with the plugin install.

One manual step remains: the grill-me companion skill. It ships via skills.sh
(not as a Claude Code plugin), so install it separately and select `grill-me`:

    npx skills@latest add mattpocock/skills

Installed skills (namespaced by the plugin):
    /disciplined-delivery:disciplined-delivery
    /disciplined-delivery:scaffold-agentic-app
EOF
