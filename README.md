Real-Time Intelligent Data Stream Query Assistant (Phase 1)

Quickstart

Local (Python)
- python3 -m venv .venv && source .venv/bin/activate
- python -m pip install --upgrade pip
- python -m pip install -e '.[dev]'
- uvicorn app.api.main:app --reload
- Visit http://localhost:8000 and http://localhost:8000/health

Docker (Compose)
- docker compose up --build
- Visit http://localhost:8000/health

Project layout (key parts)
- app/mcp: Minimal MCP host, tool registry, tools, and types
- app/services: Query engine, fraud engine, cache, LLM clients (stubs)
- app/api: FastAPI app with health route
- pyproject.toml: Dependencies and build config
- docker-compose.yml: API + Redis for cache

Next steps
- Implement query_engine.get_account_transactions
- Implement fraud_engine.analyze (query-first, context-aware)
- Wire MCP tools to services instead of placeholders

