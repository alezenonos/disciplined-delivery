# Reference architecture: production agentic / RAG app

Annotated layout the generator produces. The shape is a RAG application with an agentic
orchestration layer: a request flows through **input guardrail → query rewrite/route →
retrieval (hybrid + rerank) → context guardrail → agent orchestration (tools) → LLM →
output guardrail**, with tracing and cost tracking wrapped around every stage.

## Tree

```
production-ai-app/
├── app/
│   ├── main.py             # FastAPI entry: app, /chat + /health, schema wiring
│   ├── config.py           # Pydantic Settings from the environment
│   ├── schemas.py          # ChatRequest / Source / ChatResponse models
│   ├── Dockerfile          # API service image
│   ├── components/         # Retrieval layer
│   │   ├── retriever.py    #   hybrid (dense + sparse) search
│   │   └── reranker.py     #   cross-encoder reranking
│   ├── services/           # Core business logic
│   │   ├── llm.py          #   provider-agnostic LLM client
│   │   ├── semantic_cache.py   # answer cache keyed by embedding similarity
│   │   ├── conversation.py     # multi-turn memory + summarisation
│   │   ├── query_rewriter.py   # expand/clarify the query for retrieval
│   │   └── query_router.py     # pick handling strategy (retrieve/tool/direct)
│   ├── prompts/            # Versioned, hot-swappable prompts
│   │   ├── system.py       #   the prompt templates themselves
│   │   └── registry.py     #   resolve a prompt by name + version
│   ├── agent/              # Intelligence/orchestration layer
│   │   ├── orchestrator.py     # drives the end-to-end pipeline for one turn
│   │   ├── query_decomposer.py # split complex queries into sub-questions
│   │   ├── adaptive_router.py  # LLM-driven source/tool selection per sub-question
│   │   └── tools/          # Pluggable tool definitions
│   │       ├── web_search.py
│   │       └── code_search.py
│   ├── eval/               # Guardrails (three layers)
│   │   ├── input_quality.py    # validate/sanitise the incoming query
│   │   ├── context_filter.py   # drop irrelevant/unsafe retrieved context
│   │   └── output_quality.py   # check the answer before returning it
│   ├── tracing/            # Observability
│   │   ├── tracing.py      #   per-stage spans
│   │   ├── feedback.py     #   capture user feedback
│   │   └── cost_tracker.py #   token/$ cost per request
│   ├── data/               # raw → processed → index_config (kept via .gitkeep)
│   ├── scripts/            # seed.py, migrate.py, healthcheck.py
│   └── ui/                 # app.py + Dockerfile (chat UI calling the API)
├── tests/                  # test_retrieval / test_cache / test_routing (CI-ready)
├── architecture.md  api-reference.md  deployment.md
├── CLAUDE.md  AGENTS.md  README.md            # AI agent context + human readme
├── requirements.txt  pyproject.toml
├── Dockerfile  docker-compose.yml
├── .env.example  .gitignore
└── .github/workflows/ci.yml
```

## Why these layers

- **Separation of concerns** — retrieval (`components`), business logic (`services`), and
  orchestration (`agent`) stay independent so each can be tested and swapped in isolation.
- **Guardrails as first-class code** (`eval`) — input, context, and output are checked at
  distinct points rather than buried inside the LLM call.
- **Observability built in** (`tracing`) — tracing, feedback, and cost are present from day
  one, not bolted on after an incident.
- **Versioned prompts** (`prompts`) — prompts are data with versions, never inline strings
  scattered across modules.

## Gaps filled beyond the original diagram

The source diagram omitted a few things that a working repo needs; the generator adds them:

- **`__init__.py`** in every Python package so imports resolve.
- **`app/schemas.py`** — the Pydantic models `main.py` depends on (the diagram referenced
  schemas in a comment but shipped no file).
- **`.env.example`, `README.md`, `.gitignore`** — onboarding and hygiene basics.
- **`.github/workflows/ci.yml`** — the diagram labelled tests "CI-ready" but had no CI.
- **`Dockerfile`** — the diagram showed `Dockerfile.py` (a typo); a Dockerfile has no
  extension.
- **`data/{raw,processed,index_config}/.gitkeep`** — so the empty data dirs are tracked.

## Adapting for non-RAG agentic systems

This template is RAG-centric. For a pure tool-use or multi-agent system with little/no
retrieval, drop or thin out `app/components/` (retriever/reranker) and invest in `app/agent/`
instead — e.g. add `agents/` for multiple specialised agents, a `state.py`/`memory.py` for
shared state, and a `planner.py`. The guardrail, tracing, prompt, and service layers stay
the same.
