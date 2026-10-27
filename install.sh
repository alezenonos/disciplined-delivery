#!/usr/bin/env bash
#
# Install the disciplined-delivery plugin and its companions.
#
# Installs:
#   - disciplined-delivery + scaffold-agentic-app skills (this plugin)
#   - superpowers (auto-resolved dependency, from the official marketplace)
# Then prints the manual step for the companion skills (grilling, domain-modeling).
#
# Usage: ./install.sh
set -euo pipefail

if ! command -v claude >/dev/null 2>&1; then
  echo "error: the 'claude' CLI was not found on PATH." >&2
  echo "Install Claude Code first: https://code.claude.com/docs" >&2
  exit 1
fi

echo "==> Adding the official marketplace (superpowers dependency source)"
echo "    A dependency from a marketplace you have not added is left unresolved,"
echo "    so this must come before installing the plugin."
claude plugin marketplace add anthropics/claude-plugins-official

echo "==> Adding this marketplace"
claude plugin marketplace add alezenonos/disciplined-delivery

echo "==> Installing disciplined-delivery (auto-resolves the superpowers dependency)"
claude plugin install disciplined-delivery@alezenonos

cat <<'EOF'

==> Done with the plugin install.

The companion skills install separately (they ship via skills.sh, not as a plugin):

  - grilling + domain-modeling:
      npx skills@latest add mattpocock/skills        # select grilling and domain-modeling

The pre-PR review uses Claude Code's built-in /code-review; nothing to install.

Installed skills (namespaced by the plugin):
    /disciplined-delivery:disciplined-delivery
    /disciplined-delivery:scaffold-agentic-app
EOF
