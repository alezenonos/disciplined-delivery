---
name: scaffold-agentic-app
description: Use when starting/bootstrapping a NEW production agentic or RAG LLM application from scratch — "scaffold an agentic app", "set up a production LLM project structure", "create the directory layout for a RAG service". Generates the full tree with light placeholder code. Not for adding to an existing app.
---

# Scaffold Agentic App

## Overview

One-shot bootstrap of an opinionated, production-shaped **RAG application with an agentic
layer** (Python + FastAPI). It writes the full directory tree with **light runnable
stubs** — every module has imports, signatures, docstrings explaining its role, and `TODO`
markers. The app boots; the logic is intentionally stubbed.

This is a **greenfield-only** companion to `disciplined-delivery`. It is a deliberate
exception to that skill's small-increment loop: the scaffold is the *starting point*, not
a reviewed change. Once it exists, **hand off to `disciplined-delivery`** and build every
feature as a small, test-first, individually reviewed increment.

## When to use

- The user is starting a new agentic/RAG LLM project and wants a sane structure.
- They reference "the production-ai-app layout" or a similar reference architecture.

Not for: an existing codebase (it never overwrites files, but it also won't restructure
one), throwaway spikes, or non-Python stacks.

## How to invoke

Run the bundled generator, passing the target directory (defaults to `production-ai-app`).
The generator lives alongside this skill, so reference it via `${CLAUDE_SKILL_DIR}`:

```bash
python "${CLAUDE_SKILL_DIR}/scaffold.py" path/to/production-ai-app
```

It is **idempotent and safe**: existing files are skipped and reported, never overwritten.
Re-running only fills in what is missing. The exception is project-memory files (`CLAUDE.md`,
`AGENTS.md`): if one already exists, the generator **appends** its block once (under markers)
rather than skipping, so a project's own memory is preserved. Exit code is non-zero only on a
real error.

## What it produces

The tree below. See `references/structure.md` for the per-module purpose and the rationale
behind each gap that was filled beyond the original diagram.

```
<target>/
├── app/
│   ├── main.py config.py schemas.py Dockerfile
│   ├── components/   retriever.py reranker.py            # hybrid search + rerank
│   ├── services/     llm.py semantic_cache.py conversation.py query_rewriter.py query_router.py
│   ├── prompts/      system.py registry.py               # versioned, hot-swappable
│   ├── agent/        orchestrator.py query_decomposer.py adaptive_router.py
│   │   └── tools/    web_search.py code_search.py        # pluggable tools
│   ├── eval/         input_quality.py context_filter.py output_quality.py   # guardrails
│   ├── tracing/      tracing.py feedback.py cost_tracker.py
│   ├── data/         raw/ processed/ index_config/
│   ├── scripts/      seed.py migrate.py healthcheck.py
│   └── ui/           app.py Dockerfile
├── tests/            test_retrieval.py test_cache.py test_routing.py
├── architecture.md api-reference.md deployment.md
├── CLAUDE.md AGENTS.md README.md
├── requirements.txt pyproject.toml Dockerfile docker-compose.yml
├── .env.example .gitignore
└── .github/workflows/ci.yml
```

## After scaffolding

1. `cp .env.example .env` and fill in keys.
2. `pip install -r requirements.txt` then `uvicorn app.main:app --reload`; hit `GET /health`.
3. From here, use **`disciplined-delivery`** for every change: one focused, test-first,
   reviewable increment at a time. Replace `raise NotImplementedError` stubs as you go,
   un-skipping the matching tests in `tests/`.
