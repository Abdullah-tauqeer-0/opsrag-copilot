from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from app.db import models

router = APIRouter()

@router.get("")
def audit(workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Admin")
    logs = db.query(models.AuditLog).filter_by(workspace_id=workspace_id).all()
    return [{"id": l.id, "event": l.event_type, "payload": l.payload_json, "at": str(l.created_at)} for l in logs]
