from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from worker.tasks.ingest import ingest_document
from app.audit.logger import log_event

router = APIRouter()

@router.post("/upload")
def upload_doc(workspace_id: int, file: UploadFile, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Member")
    content = file.file.read().decode("utf-8", errors="ignore")
    doc = models.Document(workspace_id=workspace_id, source="upload", title=file.filename, status="uploaded")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    log_event(db, workspace_id, user.id, "doc_uploaded", {"doc_id": doc.id, "title": doc.title})
    ingest_document.delay(doc.id, content)
    return {"id": doc.id, "status": doc.status}

@router.post("/ingest/seed")
def ingest_seed(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Member")
    from pathlib import Path
    seed_dir = Path("/app/corpus/seed")
    for p in seed_dir.glob("*.md"):
        content = p.read_text(encoding="utf-8")
        doc = models.Document(workspace_id=workspace_id, source="seed", title=p.name, status="uploaded")
        db.add(doc)
        db.commit()
        db.refresh(doc)
        log_event(db, workspace_id, user.id, "doc_uploaded", {"doc_id": doc.id, "title": doc.title})
        ingest_document.delay(doc.id, content)
    return {"ok": True}

@router.get("")
def list_docs(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Viewer")
    docs = db.query(models.Document).filter_by(workspace_id=workspace_id).all()
    return [{"id": d.id, "title": d.title, "status": d.status} for d in docs]

@router.get("/{id}")
def get_doc(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    d = db.query(models.Document).filter_by(id=id).first()
    return {"id": d.id, "title": d.title, "status": d.status}
