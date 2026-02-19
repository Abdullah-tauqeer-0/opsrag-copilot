from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from app.db import models
from app.tools.mock import run_tool
from app.audit.logger import log_event

router = APIRouter()

@router.get("")
def list_approvals(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    approvals = db.query(models.Approval).filter_by(workspace_id=workspace_id).all()
    return [{"id": a.id, "status": a.status, "proposed": a.proposed_tool_calls_json} for a in approvals]

@router.post("/{id}/approve")
def approve(id: int, workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    a = db.query(models.Approval).filter_by(id=id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    calls = a.edited_tool_calls_json or a.proposed_tool_calls_json
    a.status = "approved"
    a.decision_by = user.id
    db.commit()
    log_event(db, workspace_id, user.id, "approval_decision", {"approval_id": a.id, "status": "approved"})
    results = []
    for call in calls:
        out = run_tool(db, workspace_id, call["tool"], call["input"])
        tr = models.ToolRun(approval_id=a.id, tool_name=call["tool"], input_json=call["input"], output_json=out, status="success")
        db.add(tr)
        log_event(db, workspace_id, user.id, "tool_run", {"tool": call["tool"], "input": call["input"], "output": out})
        results.append(out)
    db.commit()
    return {"ok": True, "results": results}

@router.post("/{id}/reject")
def reject(id: int, workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    a = db.query(models.Approval).filter_by(id=id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    a.status = "rejected"
    a.decision_by = user.id
    db.commit()
    log_event(db, workspace_id, user.id, "approval_decision", {"approval_id": a.id, "status": "rejected"})
    return {"ok": True}

@router.post("/{id}/edit-and-approve")
def edit_and_approve(id: int, workspace_id: int, edited: list, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    a = db.query(models.Approval).filter_by(id=id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    a.edited_tool_calls_json = edited
    db.commit()
    return approve(id, workspace_id, db, user)
