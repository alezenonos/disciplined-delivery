# disciplined-delivery

A Claude Code plugin with two skills:

- **`disciplined-delivery`** — ship work as small, test-first, individually reviewable
  increments, with the human as the gate that commits and merges.
- **`scaffold-agentic-app`** — one-shot scaffolder for a production RAG/agentic LLM app
  (Python + FastAPI) with light placeholder code.

## Install

This plugin depends on obra's [`superpowers`](https://github.com/obra/superpowers) plugin,
which lives in a different marketplace. Add that marketplace **first** so the dependency
resolves automatically (a dependency from a marketplace you have not added is left
unresolved):

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin marketplace add alezenonos/disciplined-delivery
/plugin install disciplined-delivery@alezenonos
```

Installing the plugin auto-resolves and installs `superpowers` (cross-marketplace install
is permitted by `allowCrossMarketplaceDependenciesOn` in this repo's `marketplace.json`).

### Also recommended: grill-me

The `disciplined-delivery` skill uses the `grill-me` skill to stress-test load-bearing
decisions. It ships via `skills.sh`, not as a Claude Code plugin, so install it separately:

```bash
npx skills@latest add mattpocock/skills   # then select grill-me
```

## Skills

Once installed, the skills are namespaced by the plugin:

- `/disciplined-delivery:disciplined-delivery`
- `/disciplined-delivery:scaffold-agentic-app`

Claude also loads them automatically when a task matches their description.

## Layout

```
.claude-plugin/
  plugin.json         # plugin manifest + dependencies
  marketplace.json    # marketplace catalog (self-hosts this plugin)
skills/
  disciplined-delivery/SKILL.md
  scaffold-agentic-app/SKILL.md  scaffold.py  references/structure.md
```
