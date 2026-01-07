from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from app.db import models
import json
from pathlib import Path

router = APIRouter()

@router.post("/run")
def run_eval(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    p = Path("/app/eval/results/latest.json")
    if not p.exists():
        return {"ok": False}
    metrics = json.loads(p.read_text(encoding="utf-8"))
    run = models.EvalRun(workspace_id=workspace_id, metrics_json=metrics)
    db.add(run)
    db.commit()
    return {"ok": True, "metrics": metrics}

@router.get("/latest")
def latest_eval(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Viewer")
    run = db.query(models.EvalRun).filter_by(workspace_id=workspace_id).order_by(models.EvalRun.id.desc()).first()
    if not run:
        return {"metrics": None}
    return {"metrics": run.metrics_json}
