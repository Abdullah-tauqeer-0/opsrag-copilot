# opsrag-copilot

A multi-tenant Enterprise Copilot that provides grounded RAG answers with citations and safe, human-approved tool actions.

**Goal**: RAG + agent actions with RBAC, audit logs, eval, and observability. Runs locally with one command.

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

**Security Notes**
- Retrieved text is untrusted; tool calls must be user-requested and admin-approved.
- Tool allowlist and schema validation.
- Audit logs store key events (no secrets).

**Screenshots**
- `docs/screenshots/chat.png`
- `docs/screenshots/approvals.png`
- `docs/screenshots/audit.png`
