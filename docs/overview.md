# opsrag-copilot Overview

opsrag-copilot is a production-style, multi-tenant RAG copilot with approvals, audit trails, and evals. It is designed to feel like an enterprise system while remaining easy to run locally. ✨

**What It Is**
- A full-stack, local-ready RAG copilot with citations and grounded answers. 🔎
- A safe agent flow that requires human approvals for tool actions. ✅
- A realistic stack for engineering workflows: UI, API, DB, cache, worker, and tracing. 🧩

**Core Principles**
- Grounded responses with transparent citations. 📌
- Explicit human approval for side-effecting actions. 🛡️
- Auditability and observability by default. 📈

**Architecture At A Glance**
- UI: Next.js app in `frontend/`.
- API: FastAPI service in `backend/`.
- Storage: Postgres + pgvector for hybrid retrieval.
- Cache/Queue: Redis + Celery for async tasks and ingestion.
- Tracing: Jaeger for distributed traces.

**Prerequisites**
- Docker Desktop (or Docker Engine) running locally.
- `make` available in your shell.
- Python 3.11+ if you want to run scripts directly. 🐍

**Quickstart**
1. Copy the environment template:
   - `cp .env.example .env`
2. Start the full stack:
   - `make demo`
3. Open the UI:
   - `http://localhost:3000`
4. Log in with the demo credentials printed by `make demo`. 🚀

**Demo Credentials**
- Admin: `admin@demo.local` / `admin123`
- Member: `member@demo.local` / `member123`
- Viewer: `viewer@demo.local` / `viewer123`

**How RAG Works**
The system uses hybrid retrieval. Lexical matching via Postgres `ts_rank` is combined with vector similarity from pgvector. Scores are fused, then optionally reranked. Answers include citations with document name, chunk id, and snippet for traceability. ⚖️

**Agent + Approvals Flow**
- The agent proposes tool calls as structured JSON.
- An approval request is created and reviewed by an Admin.
- Approved actions execute in mock tools by default.
- All actions are recorded in audit logs. 🧾

**Common Commands**
- `make demo`: start UI, API, DB, cache, worker, and tracing.
- `make eval`: run the offline evaluation suite.
- `python scripts/bootstrap_demo.py`: seed demo data and users.
- `python scripts/build_eval_dataset.py`: build eval datasets.
- `python scripts/run_eval.py`: run evals and write a report.

**Working With Data**
- Seed documents live in `corpus/seed/`.
- Processed documents go in `corpus/processed/`.
- Eval datasets live in `eval/datasets/`.
- Download the full NIST AI RMF corpus with:
  - `python scripts/fetch_nist_corpus.py` 📚

**Configuration**
Environment variables are defined in `.env.example`. Copy to `.env` and edit as needed. The demo defaults are designed for local use only. 🔧

**Troubleshooting**
- If services fail to start, ensure Docker is running and ports are free.
- For DB issues, confirm Postgres and pgvector are healthy in `docker-compose`.
- If the UI is blank, check the API container logs for startup errors.

**Security Notes**
- Retrieved text is untrusted; approvals protect against unsafe tool actions.
- Tool allowlists and schema validation reduce risk.
- Audit logs are designed to capture key events without secrets. 🔒

**Where To Look Next**
- UI routes: `frontend/app/`
- API endpoints: `backend/app/api/`
- Retrieval logic: `backend/app/retrieval/`
- Approvals and audit: `backend/app/api/approvals.py`, `backend/app/api/audit.py`
