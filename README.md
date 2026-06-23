# disciplined-delivery

A Claude Code plugin with two skills:

- **`disciplined-delivery`** — ship work as small, test-first, individually reviewable
  increments, with the human as the gate that commits and merges.
- **`scaffold-agentic-app`** — one-shot scaffolder for a production RAG/agentic LLM app
  (Python + FastAPI) with light placeholder code.

## Install

> **Pointing an AI agent (Claude Code) at this repo?** Tell it: *"Install the skills
> from this repo following the README."* The four commands below, run in order, install
> everything: this plugin's two skills, the `superpowers` dependency, and the `grill-me`
> companion.

### Quick install (one shot)

From a checkout of this repo:

```bash
./install.sh
```

It adds both marketplaces, installs the plugin (which auto-pulls `superpowers`), and prints
the one remaining `grill-me` step.

### Manual install

Run inside Claude Code (slash commands) **or** in a terminal (prefix each with `claude `):

```bash
# 1. Add obra's marketplace FIRST — a dependency from a marketplace you have not
#    added is left unresolved.
/plugin marketplace add obra/superpowers-marketplace

# 2. Add this marketplace and install the plugin. This auto-resolves and installs
#    `superpowers` (cross-marketplace install is permitted by
#    allowCrossMarketplaceDependenciesOn in this repo's marketplace.json).
/plugin marketplace add alezenonos/disciplined-delivery
/plugin install disciplined-delivery@alezenonos

# 3. Install the grill-me companion skill. It ships via skills.sh (not a Claude Code
#    plugin), so it is a separate step:
npx skills@latest add mattpocock/skills   # then select grill-me
```

Terminal equivalents: `claude plugin marketplace add …` and `claude plugin install …`.

### What gets installed

| Component | Source | How |
| --- | --- | --- |
| `disciplined-delivery` skill | this repo | plugin install |
| `scaffold-agentic-app` skill | this repo | plugin install |
| `superpowers` (brainstorming, writing-plans, TDD, verification) | obra/superpowers-marketplace | auto-resolved dependency |
| `grill-me` | mattpocock/skills (`skills.sh`) | `npx skills@latest add` |

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
