from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, workspaces, docs, chat, retrieval, approvals, audit, evals
from app.observability.tracing import setup_tracing
from app.observability.metrics import setup_metrics

app = FastAPI(title="opsrag-copilot")

setup_tracing(app)
setup_metrics(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
app.include_router(docs.router, prefix="/docs", tags=["docs"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
app.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
app.include_router(audit.router, prefix="/audit", tags=["audit"])
app.include_router(evals.router, prefix="/eval", tags=["eval"])
