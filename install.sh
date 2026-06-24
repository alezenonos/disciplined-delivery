#!/usr/bin/env bash
#
# Install the disciplined-delivery plugin and its companions.
#
# Installs:
#   - disciplined-delivery + scaffold-agentic-app skills (this plugin)
#   - superpowers (auto-resolved dependency, from obra's marketplace)
# Then prints the manual steps for the companion skills (grill-with-docs, code-review-skill).
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

Two companion skills install separately (neither is a Claude Code plugin):

  - grill-with-docs (via skills.sh):
      npx skills@latest add mattpocock/skills        # select grill-with-docs

  - code-review-skill (bare skill, via git clone):
      git clone https://github.com/awesome-skills/code-review-skill.git \
        ~/.claude/skills/code-review-skill

Installed skills (namespaced by the plugin):
    /disciplined-delivery:disciplined-delivery
    /disciplined-delivery:scaffold-agentic-app
EOF
