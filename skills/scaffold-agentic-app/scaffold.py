#!/usr/bin/env python3
"""Scaffold a production agentic / RAG LLM application.

Creates an opinionated, RAG-centric project tree (Python + FastAPI) with light
runnable stubs: every module has imports, signatures, docstrings describing its
role, and TODO markers. The app boots; the logic is stubbed.

Usage:
    python scaffold.py [target_dir]

`target_dir` defaults to ``production-ai-app`` in the current directory.

The generator is idempotent and safe: it never overwrites an existing file. Files
that already exist are skipped and reported. The one exception is project-memory
files (``CLAUDE.md``, ``AGENTS.md``): if one already exists, the generator appends
its block once (under markers) instead of skipping, so a project's own memory is
preserved, not clobbered. Exit code is non-zero only on a real error (e.g. a path
component collides with an existing file).
"""
from __future__ import annotations

import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
# Reusable stub bodies
# --------------------------------------------------------------------------- #

PKG_INIT = '"""Package marker. TODO: export the package public API here."""\n'


def _module(summary: str, body: str = "") -> str:
    """Build a light module stub with a one-line summary docstring."""
    return f'"""{summary}\n\nTODO: implement. This is a scaffold stub.\n"""\n{body}'


# --------------------------------------------------------------------------- #
# The template: relative path -> file contents.
# Order matters only for readability; directories are created implicitly.
# A trailing empty string for a ``.gitkeep`` keeps an otherwise-empty dir.
# --------------------------------------------------------------------------- #

# The README's first line; ``scaffold`` replaces it with the target directory's name.
README_TITLE = "# production-ai-app\n"

FILES: dict[str, str] = {
    # ---- top-level project files -------------------------------------------------
    "README.md": (
        f"{README_TITLE}\n"
        "Production RAG-style LLM application with an agentic layer. Scaffolded by the\n"
        "`scaffold-agentic-app` skill. See `architecture.md` for the design and\n"
        "`deployment.md` to run it.\n\n"
        "## Quick start\n\n"
        "```bash\n"
        "cp .env.example .env        # fill in your keys\n"
        "pip install -r requirements.txt\n"
        "uvicorn app.main:app --reload\n"
        "```\n\n"
        "Health check: `GET http://localhost:8000/health`.\n\n"
        "## Layout\n\n"
        "- `app/components` — retrieval (hybrid search + reranking)\n"
        "- `app/services` — core business logic (LLM, cache, memory, rewriting, routing)\n"
        "- `app/prompts` — versioned, hot-swappable prompts\n"
        "- `app/agent` — orchestration, decomposition, adaptive routing, pluggable tools\n"
        "- `app/eval` — input / context / output guardrails\n"
        "- `app/tracing` — tracing, feedback capture, cost tracking\n"
        "- `tests` — config / health tests that run, plus retrieval / cache / routing\n"
        "  stubs to un-skip as you build\n\n"
        "Checks (the ones CI runs): `ruff check . && pytest`.\n\n"
        "After scaffolding, make all further changes as small, test-first, reviewed\n"
        "increments (see the `disciplined-delivery` skill).\n"
    ),
    ".env.example": (
        "# Copy to .env and fill in. Never commit real secrets.\n"
        "APP_ENV=development\n"
        "LOG_LEVEL=info\n"
        "LLM_PROVIDER=anthropic\n"
        "# LLM_MODEL=   # optional override; the default lives in app/config.py only\n"
        "ANTHROPIC_API_KEY=\n"
        "# Vector store / search backends\n"
        "VECTOR_DB_URL=\n"
        "SEMANTIC_CACHE_URL=\n"
    ),
    ".dockerignore": (
        "# Keep secrets and local state out of the build context: the Dockerfiles `COPY . .`.\n"
        ".env\n.env.*\n!.env.example\n"
        ".git/\n.venv/\nvenv/\n__pycache__/\n*.py[cod]\n"
        ".pytest_cache/\n.mypy_cache/\n.ruff_cache/\n"
    ),
    ".gitignore": (
        "__pycache__/\n*.py[cod]\n.venv/\nvenv/\n.env\n.pytest_cache/\n"
        ".mypy_cache/\n.ruff_cache/\n*.egg-info/\ndist/\nbuild/\n"
        "app/data/raw/*\napp/data/processed/*\n!app/data/**/.gitkeep\n"
    ),
    "requirements.txt": (
        "fastapi>=0.110\n"
        "uvicorn[standard]>=0.29\n"
        "pydantic>=2.6\n"
        "pydantic-settings>=2.2\n"
        "httpx>=0.27\n"
        "# dev tools: the tests and the linter CI runs\n"
        "pytest>=8.0\n"
        "ruff>=0.6\n"
    ),
    "pyproject.toml": (
        "[project]\n"
        'name = "production-ai-app"\n'
        'version = "0.1.0"\n'
        'description = "Production RAG-style LLM app with an agentic layer."\n'
        'requires-python = ">=3.11"\n\n'
        "[tool.pytest.ini_options]\n"
        'testpaths = ["tests"]\n\n'
        "[tool.ruff]\n"
        "line-length = 100\n\n"
        "[tool.ruff.lint]\n"
        "# The style standard, enforced by the linter in CI: PEP-8 (E/W), pyflakes (F),\n"
        "# import order (I), naming (N), Google-style docstrings (D), modern idioms (UP),\n"
        "# common bugs (B).\n"
        'select = ["E", "W", "F", "I", "N", "D", "UP", "B"]\n\n'
        "[tool.ruff.lint.pydocstyle]\n"
        'convention = "google"\n\n'
        "[tool.ruff.lint.per-file-ignores]\n"
        "# Test names are the documentation; every other rule still applies to tests.\n"
        '"tests/**" = ["D"]\n'
    ),
    "Dockerfile": (
        "FROM python:3.11-slim\n"
        "WORKDIR /srv\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]\n'
    ),
    "docker-compose.yml": (
        "services:\n"
        "  api:\n"
        "    build: .\n"
        '    ports: ["8000:8000"]\n'
        "    env_file: .env\n"
        "  ui:\n"
        "    build:\n"
        "      context: .\n"
        "      dockerfile: app/ui/Dockerfile\n"
        '    ports: ["8501:8501"]\n'
        "    env_file: .env\n"
        "    depends_on: [api]\n"
    ),
    "CLAUDE.md": (
        "# Project memory for AI coding agents\n\n"
        "Production RAG-style LLM app with an agentic layer.\n\n"
        "## Rules\n"
        "- Ship small, test-first, individually reviewable changes (see `disciplined-delivery`).\n"
        "- Keep retrieval (`app/components`), business logic (`app/services`), and\n"
        "  orchestration (`app/agent`) separate.\n"
        "- Guardrails live in `app/eval`; observability in `app/tracing`.\n"
        "- Prompts are versioned in `app/prompts` — never inline prompt strings elsewhere.\n\n"
        "## TODO\n"
        "- Fill in stack-specific conventions, commands, and gotchas.\n"
    ),
    "AGENTS.md": (
        "# Agent context\n\n"
        "Conventions for autonomous/coding agents working in this repo. Mirror anything\n"
        "load-bearing into `CLAUDE.md`. TODO: document tool contracts and guardrails.\n"
    ),
    "architecture.md": (
        "# Architecture\n\n"
        "Request flow: **input guardrail → query rewrite/route → retrieval (hybrid +\n"
        "rerank) → context guardrail → agent orchestration (tools) → LLM → output\n"
        "guardrail**, with tracing and cost tracking around every stage.\n\n"
        "## Layers\n"
        "| Layer | Package | Responsibility |\n"
        "| --- | --- | --- |\n"
        "| Retrieval | `app/components` | Hybrid search + reranking |\n"
        "| Services | `app/services` | LLM, semantic cache, memory, rewrite, route |\n"
        "| Prompts | `app/prompts` | Versioned, hot-swappable templates |\n"
        "| Agent | `app/agent` | Orchestration, decomposition, adaptive routing, tools |\n"
        "| Eval | `app/eval` | Input / context / output guardrails |\n"
        "| Tracing | `app/tracing` | Spans, feedback, cost |\n\n"
        "TODO: expand with sequence diagrams and failure modes.\n"
    ),
    "api-reference.md": (
        "# API reference\n\n"
        "## `POST /chat`\n"
        "Request: `ChatRequest` — `{ \"message\": str, \"session_id\": str | null }`.\n"
        "Response: `ChatResponse` — "
        "`{ \"answer\": str, \"sources\": list, \"trace_id\": str }`.\n\n"
        "## `GET /health`\n"
        "Liveness probe. Returns `{ \"status\": \"ok\", \"env\": str }` (`env` is `APP_ENV`).\n\n"
        "TODO: document auth, rate limits, and error shapes.\n"
    ),
    "deployment.md": (
        "# Deployment\n\n"
        "```bash\n"
        "docker compose up --build\n"
        "```\n\n"
        "API on `:8000`, UI on `:8501`. TODO: document the target platform, secrets\n"
        "management, migrations (`app/scripts/migrate.py`), and health checks.\n"
    ),
    ".github/workflows/ci.yml": (
        "name: CI\n"
        "on:\n"
        "  push:\n"
        "  pull_request:\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      # Pinned to a commit; .github/dependabot.yml keeps the pins current.\n"
        "      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1\n"
        "      - uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0\n"
        '        with: { python-version: "3.11" }\n'
        "      - run: pip install -r requirements.txt\n"
        "      - run: ruff check .\n"
        "      - run: python -m compileall -q app\n"
        "      - run: pytest\n"
    ),
    ".github/dependabot.yml": (
        "version: 2\n"
        "updates:\n"
        "  - package-ecosystem: github-actions\n"
        '    directory: "/"\n'
        "    schedule:\n"
        "      interval: weekly\n"
        "  - package-ecosystem: pip\n"
        '    directory: "/"\n'
        "    schedule:\n"
        "      interval: weekly\n"
    ),
    # ---- app package -------------------------------------------------------------
    "app/__init__.py": PKG_INIT,
    "app/main.py": (
        '"""FastAPI entrypoint: app factory, routes, schemas wiring."""\n'
        "from __future__ import annotations\n\n"
        "from fastapi import FastAPI\n\n"
        "from app.config import settings\n"
        "from app.schemas import ChatRequest, ChatResponse\n\n"
        "app = FastAPI(title=\"production-ai-app\", version=\"0.1.0\")\n\n\n"
        "@app.get(\"/health\")\n"
        "def health() -> dict[str, str]:\n"
        '    """Liveness probe."""\n'
        '    return {"status": "ok", "env": settings.app_env}\n\n\n'
        "@app.post(\"/chat\", response_model=ChatResponse)\n"
        "async def chat(request: ChatRequest) -> ChatResponse:\n"
        '    """Handle a chat turn.\n\n'
        "    TODO: wire input guardrail -> rewrite/route -> retrieve -> context\n"
        "    guardrail -> agent orchestration -> LLM -> output guardrail, with tracing.\n"
        '    """\n'
        "    # from app.agent.orchestrator import Orchestrator\n"
        "    # return await Orchestrator().run(request)\n"
        "    raise NotImplementedError(\"chat pipeline not implemented yet\")\n"
    ),
    "app/config.py": (
        '"""Application settings, loaded from the environment."""\n'
        "from __future__ import annotations\n\n"
        "from pydantic import SecretStr\n"
        "from pydantic_settings import BaseSettings, SettingsConfigDict\n\n\n"
        "class Settings(BaseSettings):\n"
        '    """Typed configuration, validated on load.\n\n'
        "    An unknown key in ``.env`` is rejected (``extra=\"forbid\"``), so a typo cannot\n"
        "    read as configured while the default silently stays in force. Declare a field\n"
        "    here before adding its key to ``.env.example``; ``tests/test_config.py`` checks\n"
        "    the two agree. TODO: add feature flags.\n"
        '    """\n\n'
        "    model_config = SettingsConfigDict(env_file=\".env\", extra=\"forbid\")\n\n"
        "    app_env: str = \"development\"\n"
        "    log_level: str = \"info\"\n"
        "    llm_provider: str = \"anthropic\"\n"
        "    # The model default's only home. A pinned model id goes stale: check it is\n"
        "    # still live in your provider's model list before relying on it.\n"
        "    llm_model: str = \"claude-opus-5-5\"\n"
        "    anthropic_api_key: SecretStr = SecretStr(\"\")\n"
        "    vector_db_url: str = \"\"\n"
        "    semantic_cache_url: str = \"\"\n\n\n"
        "settings = Settings()\n"
    ),
    "app/schemas.py": (
        '"""Pydantic request/response models shared across the API."""\n'
        "from __future__ import annotations\n\n"
        "from pydantic import BaseModel\n\n\n"
        "class ChatRequest(BaseModel):\n"
        '    """One user turn sent to ``POST /chat``."""\n\n'
        "    message: str\n"
        "    session_id: str | None = None\n\n\n"
        "class Source(BaseModel):\n"
        '    """A retrieved document cited in an answer."""\n\n'
        "    title: str\n"
        "    url: str | None = None\n"
        "    score: float | None = None\n\n\n"
        "class ChatResponse(BaseModel):\n"
        '    """The answer to one turn, with its sources and trace id."""\n\n'
        "    answer: str\n"
        "    sources: list[Source] = []\n"
        "    trace_id: str | None = None\n"
    ),
    # ---- components: retrieval ---------------------------------------------------
    "app/components/__init__.py": PKG_INIT,
    "app/components/retriever.py": _module(
        "Hybrid retriever: combine dense (vector) and sparse (keyword) search.",
        "from __future__ import annotations\n\n\n"
        "class HybridRetriever:\n"
        '    """Retrieve candidate documents via dense + sparse search."""\n\n'
        "    def retrieve(self, query: str, k: int = 10) -> list[dict]:\n"
        '        """Return the top ``k`` candidates for ``query``."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/components/reranker.py": _module(
        "Cross-encoder reranker: reorder retrieved candidates by relevance.",
        "from __future__ import annotations\n\n\n"
        "class Reranker:\n"
        '    """Reorder retrieved candidates with a cross-encoder."""\n\n'
        "    def rerank(self, query: str, docs: list[dict], top_n: int = 5) -> list[dict]:\n"
        '        """Return the ``top_n`` most relevant of ``docs``."""\n'
        "        raise NotImplementedError\n",
    ),
    # ---- services: business logic ------------------------------------------------
    "app/services/__init__.py": PKG_INIT,
    "app/services/llm.py": _module(
        "LLM client wrapper: provider-agnostic completion + streaming.",
        "from __future__ import annotations\n\n\n"
        "class LLMService:\n"
        '    """Provider-agnostic LLM client."""\n\n'
        "    async def complete(self, prompt: str, **kwargs) -> str:\n"
        '        """Return the completion for ``prompt``."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/services/semantic_cache.py": _module(
        "Semantic cache: return prior answers for embedding-similar queries.",
        "from __future__ import annotations\n\n\n"
        "class SemanticCache:\n"
        '    """Answer cache keyed by embedding similarity."""\n\n'
        "    async def get(self, query: str) -> str | None:\n"
        '        """Return a cached answer for a similar query, or ``None``."""\n'
        "        raise NotImplementedError\n\n"
        "    async def set(self, query: str, answer: str) -> None:\n"
        '        """Store ``answer`` under ``query``."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/services/conversation.py": _module(
        "Conversation memory: persist and summarise multi-turn history.",
        "from __future__ import annotations\n\n\n"
        "class ConversationMemory:\n"
        '    """Multi-turn history store."""\n\n'
        "    async def history(self, session_id: str) -> list[dict]:\n"
        '        """Return the turns recorded for ``session_id``."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/services/query_rewriter.py": _module(
        "Query rewriter: expand/clarify the user query for retrieval.",
        "from __future__ import annotations\n\n\n"
        "class QueryRewriter:\n"
        '    """Rewrite a query using the conversation so far."""\n\n'
        "    async def rewrite(self, query: str, history: list[dict]) -> str:\n"
        '        """Return ``query`` expanded or clarified for retrieval."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/services/query_router.py": _module(
        "Query router: pick the handling strategy (retrieve, tool, direct).",
        "from __future__ import annotations\n\n\n"
        "class QueryRouter:\n"
        '    """Choose how a query is handled."""\n\n'
        "    async def route(self, query: str) -> str:\n"
        '        """Return the strategy name: retrieve, tool or direct."""\n'
        "        raise NotImplementedError\n",
    ),
    # ---- prompts -----------------------------------------------------------------
    "app/prompts/__init__.py": PKG_INIT,
    "app/prompts/system.py": _module(
        "System prompts: versioned, type-specific templates.",
        "SYSTEM_PROMPT_V1 = \"\"\"You are a helpful assistant. TODO: refine.\"\"\"\n",
    ),
    "app/prompts/registry.py": _module(
        "Prompt registry: resolve a prompt by name + version (hot-swappable).",
        "from __future__ import annotations\n\n\n"
        "class PromptRegistry:\n"
        '    """Lookup of prompt templates by name and version."""\n\n'
        "    def get(self, name: str, version: str = \"latest\") -> str:\n"
        '        """Return the prompt text for ``name`` at ``version``."""\n'
        "        raise NotImplementedError\n",
    ),
    # ---- agent: orchestration ----------------------------------------------------
    "app/agent/__init__.py": PKG_INIT,
    "app/agent/orchestrator.py": (
        '"""Agent orchestrator: drive the end-to-end chat pipeline.\n\n'
        "TODO: implement. This is a scaffold stub.\n"
        '"""\n'
        "from __future__ import annotations\n\n"
        "from app.schemas import ChatRequest, ChatResponse\n\n\n"
        "class Orchestrator:\n"
        '    """Coordinate guardrails, retrieval, tools, and the LLM for one turn."""\n\n'
        "    async def run(self, request: ChatRequest) -> ChatResponse:\n"
        '        """Answer one chat turn end to end."""\n'
        "        raise NotImplementedError\n"
    ),
    "app/agent/query_decomposer.py": _module(
        "Query decomposer: split a complex query into sub-questions.",
        "from __future__ import annotations\n\n\n"
        "class QueryDecomposer:\n"
        '    """Split a complex query into sub-questions."""\n\n'
        "    async def decompose(self, query: str) -> list[str]:\n"
        '        """Return the sub-questions of ``query``."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/agent/adaptive_router.py": _module(
        "Adaptive router: LLM-driven selection of sources/tools per sub-question.",
        "from __future__ import annotations\n\n\n"
        "class AdaptiveRouter:\n"
        '    """Pick sources and tools per sub-question."""\n\n'
        "    async def select(self, sub_query: str) -> list[str]:\n"
        '        """Return the names of the sources/tools to use."""\n'
        "        raise NotImplementedError\n",
    ),
    "app/agent/tools/__init__.py": PKG_INIT,
    "app/agent/tools/web_search.py": _module(
        "Pluggable tool: web search.",
        "from __future__ import annotations\n\n\n"
        "async def web_search(query: str) -> list[dict]:\n"
        '    """Search the web. TODO: wire a provider."""\n'
        "    raise NotImplementedError\n",
    ),
    "app/agent/tools/code_search.py": _module(
        "Pluggable tool: code search.",
        "from __future__ import annotations\n\n\n"
        "async def code_search(query: str) -> list[dict]:\n"
        '    """Search a codebase. TODO: wire a backend."""\n'
        "    raise NotImplementedError\n",
    ),
    # ---- eval: guardrails --------------------------------------------------------
    "app/eval/__init__.py": PKG_INIT,
    "app/eval/input_quality.py": _module(
        "Input guardrail: validate/sanitise the incoming query.",
        "from __future__ import annotations\n\n\n"
        "def check_input(message: str) -> bool:\n"
        '    """Return whether ``message`` is acceptable input."""\n'
        "    raise NotImplementedError\n",
    ),
    "app/eval/context_filter.py": _module(
        "Context guardrail: drop irrelevant/unsafe retrieved context.",
        "from __future__ import annotations\n\n\n"
        "def filter_context(docs: list[dict]) -> list[dict]:\n"
        '    """Return ``docs`` without irrelevant or unsafe entries."""\n'
        "    raise NotImplementedError\n",
    ),
    "app/eval/output_quality.py": _module(
        "Output guardrail: check the generated answer before returning it.",
        "from __future__ import annotations\n\n\n"
        "def check_output(answer: str) -> bool:\n"
        '    """Return whether ``answer`` is safe to return."""\n'
        "    raise NotImplementedError\n",
    ),
    # ---- tracing: observability --------------------------------------------------
    "app/tracing/__init__.py": PKG_INIT,
    "app/tracing/tracing.py": _module(
        "Per-stage tracing: spans around each pipeline step.",
        "from __future__ import annotations\n\n\n"
        "def start_span(name: str):\n"
        '    """Open a tracing span called ``name``."""\n'
        "    raise NotImplementedError\n",
    ),
    "app/tracing/feedback.py": _module(
        "Feedback capture: persist user thumbs-up/down and corrections.",
        "from __future__ import annotations\n\n\n"
        "def record_feedback(trace_id: str, score: int) -> None:\n"
        '    """Persist the ``score`` given for ``trace_id``."""\n'
        "    raise NotImplementedError\n",
    ),
    "app/tracing/cost_tracker.py": _module(
        "Cost tracker: accumulate token/$ cost per request.",
        "from __future__ import annotations\n\n\n"
        "class CostTracker:\n"
        '    """Running token and cost totals for one request."""\n\n'
        "    def add(self, tokens: int, model: str) -> None:\n"
        '        """Add ``tokens`` used on ``model`` to the totals."""\n'
        "        raise NotImplementedError\n",
    ),
    # ---- data --------------------------------------------------------------------
    "app/data/raw/.gitkeep": "",
    "app/data/processed/.gitkeep": "",
    "app/data/index_config/.gitkeep": "",
    # ---- scripts -----------------------------------------------------------------
    "app/scripts/__init__.py": PKG_INIT,
    "app/scripts/seed.py": _module(
        "Seed script: load initial documents into the index.",
        "from __future__ import annotations\n\n\n"
        "def main() -> None:\n"
        '    """Load the initial documents."""\n'
        "    raise NotImplementedError\n\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    ),
    "app/scripts/migrate.py": _module(
        "Migration script: apply schema/index migrations.",
        "from __future__ import annotations\n\n\n"
        "def main() -> None:\n"
        '    """Apply pending migrations."""\n'
        "    raise NotImplementedError\n\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    ),
    "app/scripts/healthcheck.py": _module(
        "Healthcheck script: probe dependencies (LLM, vector store, cache).",
        "from __future__ import annotations\n\n\n"
        "def main() -> int:\n"
        '    """Probe each dependency; return a process exit code."""\n'
        "    raise NotImplementedError\n\n\n"
        'if __name__ == "__main__":\n'
        "    raise SystemExit(main())\n",
    ),
    # ---- ui ----------------------------------------------------------------------
    "app/ui/app.py": _module(
        "Minimal UI entrypoint (e.g. Streamlit/Gradio) calling the API.",
        "from __future__ import annotations\n\n\n"
        "def main() -> None:\n"
        '    """TODO: render a chat UI that POSTs to /chat."""\n'
        "    raise NotImplementedError\n\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    ),
    "app/ui/Dockerfile": (
        "FROM python:3.11-slim\n"
        "WORKDIR /srv\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        'CMD ["python", "app/ui/app.py"]\n'
    ),
    # ---- tests -------------------------------------------------------------------
    "tests/__init__.py": PKG_INIT,
    "tests/test_config.py": (
        '"""Settings tests: configuration is validated on load."""\n'
        "from pathlib import Path\n\n"
        "import pytest\n"
        "from pydantic import ValidationError\n\n"
        "from app.config import Settings\n\n"
        "ROOT = Path(__file__).resolve().parents[1]\n\n\n"
        "def test_env_example_offers_only_declared_settings() -> None:\n"
        '    Settings(_env_file=ROOT / ".env.example")\n\n\n'
        "def test_unknown_key_in_env_file_is_rejected(tmp_path: Path) -> None:\n"
        '    env = tmp_path / ".env"\n'
        '    env.write_text("LLM_MODLE=typo\\n")\n'
        "    with pytest.raises(ValidationError):\n"
        "        Settings(_env_file=env)\n"
    ),
    "tests/test_health.py": (
        '"""API smoke test: the app boots and the liveness probe answers."""\n'
        "from fastapi.testclient import TestClient\n\n"
        "from app.config import settings\n"
        "from app.main import app\n\n\n"
        "def test_health_reports_ok_and_the_environment() -> None:\n"
        '    response = TestClient(app).get("/health")\n'
        "    assert response.status_code == 200\n"
        '    assert response.json() == {"status": "ok", "env": settings.app_env}\n'
    ),
    "tests/test_retrieval.py": (
        '"""Retrieval tests (scaffold stubs)."""\n'
        "import pytest\n\n\n"
        '@pytest.mark.skip(reason="scaffold stub")\n'
        "def test_hybrid_retriever_returns_k_results() -> None:\n"
        "    ...\n"
    ),
    "tests/test_cache.py": (
        '"""Semantic cache tests (scaffold stubs)."""\n'
        "import pytest\n\n\n"
        '@pytest.mark.skip(reason="scaffold stub")\n'
        "def test_cache_hit_on_similar_query() -> None:\n"
        "    ...\n"
    ),
    "tests/test_routing.py": (
        '"""Query routing tests (scaffold stubs)."""\n'
        "import pytest\n\n\n"
        '@pytest.mark.skip(reason="scaffold stub")\n'
        "def test_router_picks_strategy() -> None:\n"
        "    ...\n"
    ),
}


# Project-memory files: if one already exists in the target, append our block
# (once, idempotently) instead of skipping — never clobber a project's own.
APPEND_IF_EXISTS = {"CLAUDE.md", "AGENTS.md"}
_MARKER_BEGIN = "<!-- BEGIN scaffold-agentic-app -->"
_MARKER_END = "<!-- END scaffold-agentic-app -->"


def _scaffold_block(content: str) -> str:
    """Wrap generated content in idempotency markers so re-runs don't duplicate it."""
    return f"{_MARKER_BEGIN}\n{content.rstrip()}\n{_MARKER_END}\n"


def scaffold(target: Path) -> int:
    """Create the project tree under ``target``. Returns a process exit code."""
    created: list[str] = []
    appended: list[str] = []
    skipped: list[str] = []

    for rel, content in FILES.items():
        path = target / rel
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            print(f"ERROR: {path.parent} is not a directory; cannot scaffold here.")
            return 1

        if rel in APPEND_IF_EXISTS:
            block = _scaffold_block(content)
            if not path.exists():
                path.write_text(block, encoding="utf-8")
                created.append(rel)
            elif _MARKER_BEGIN in path.read_text(encoding="utf-8"):
                skipped.append(rel)  # our block is already present
            else:
                existing = path.read_text(encoding="utf-8")
                sep = "\n" if existing.endswith("\n") else "\n\n"
                path.write_text(existing + sep + block, encoding="utf-8")
                appended.append(rel)
            continue

        if path.exists():
            skipped.append(rel)
            continue
        if rel == "README.md":
            content = content.replace(README_TITLE, f"# {target.resolve().name}\n", 1)
        path.write_text(content, encoding="utf-8")
        created.append(rel)

    print(f"Scaffolded into: {target}")
    print(f"  created: {len(created)} file(s)")
    print(f"  appended to: {len(appended)} existing file(s)")
    print(f"  skipped: {len(skipped)} existing file(s)")
    for rel in appended:
        print(f"    - appended to {rel}")
    for rel in skipped:
        print(f"    - skipped {rel}")
    return 0


def main(argv: list[str]) -> int:
    """Scaffold into ``argv[1]`` (or the default dir) and return scaffold's exit code."""
    target = Path(argv[1]) if len(argv) > 1 else Path("production-ai-app")
    return scaffold(target)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
