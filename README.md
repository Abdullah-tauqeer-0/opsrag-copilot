# opsrag-copilot

A multi-tenant Enterprise Copilot that provides grounded RAG answers with citations and safe, human-approved tool actions.

**Goal**: RAG + agent actions with RBAC, audit logs, eval, and observability. Runs locally with one command.

**Docs**: See `docs/overview.md` for a full tour, setup, and operations guide.

**Quickstart**
```bash
cp .env.example .env
make demo
```

Demo credentials (printed by `make demo`):
- Admin: `admin@demo.local` / `admin123`
- Member: `member@demo.local` / `member123`
- Viewer: `viewer@demo.local` / `viewer123`

**Architecture**
```
             +---------------------+
             |     Next.js UI      |
             +----------+----------+
                        |
                        v
+-----------+   +-------+-------+     +--------------+
|  Jaeger   |<--|  FastAPI API  |<--->|  Postgres +  |
+-----------+   |  (RAG/Agent)  |     |  pgvector    |
                +-------+-------+     +--------------+
                        |
                        v
                  +-----+-----+
                  |  Redis    |
                  +-----+-----+
                        |
                        v
                  +-----+-----+
                  |  Celery   |
                  +-----------+
```

**What It Is**
- A production-style RAG copilot with multi-tenant workspaces, RBAC, and audit logging. 🧭
- A safe agent execution flow that requires human approval before tool actions. ✅
- A full local stack (UI, API, DB, cache, worker, tracing) for realistic workflows. 🧩

**Key Features**
- Grounded answers with citations and chunk-level traceability. 🔎
- Hybrid retrieval (BM25-like + vector similarity) with score fusion. ⚖️
- Approval gates for agent actions, with structured tool payloads. 🛡️
- Built-in eval harness and reports. 📊
- Observability hooks for metrics and traces. 📈

**How RAG Works**
- Hybrid retrieval: lexical BM25-like (Postgres `ts_rank`) + vector similarity (pgvector).
- Weighted score fusion and optional rerank.
- Answers include citations with document name, chunk id, and snippet.

**Agent + Approvals**
- Agent proposes tool calls as JSON and creates an approval request.
- Admin reviews, edits, approves/rejects.
- Approved actions execute in mock tools (default) and are logged.

**Eval**
- `make eval` runs offline evaluation, writes JSON + Markdown report.
- Recall@5 for retrieval and groundedness heuristic.

**Full NIST Corpus**
- Run `python scripts/fetch_nist_corpus.py` to download NIST AI RMF resources into `corpus/raw/` and process into `corpus/processed/`.

**How To Run**
- Copy env and start the stack:
  - `cp .env.example .env`
  - `make demo`
- Open the UI at `http://localhost:3000` and log in with demo credentials. 🚀

**Common Commands**
- `make demo`: starts the full stack with local services.
- `make eval`: runs offline evaluation and writes a report.
- `python scripts/bootstrap_demo.py`: seeds data and sets up demo users.
- `python scripts/build_eval_dataset.py`: builds eval dataset artifacts.

**Project Structure**
- `frontend/`: Next.js UI.
- `backend/`: FastAPI API, auth, retrieval, approvals, audit logging.
- `worker/`: Celery worker and ingestion tasks.
- `infra/`: docker-compose and infrastructure wiring.
- `corpus/`: seed and raw/processed documents.
- `eval/`: evaluation datasets and outputs.
- `docs/`: documentation and screenshots.

**Security Notes**
- Retrieved text is untrusted; tool calls must be user-requested and admin-approved.
- Tool allowlist and schema validation.
- Audit logs store key events (no secrets).

**Screenshots**
- `docs/screenshots/chat.png`
- `docs/screenshots/approvals.png`
- `docs/screenshots/audit.png`
