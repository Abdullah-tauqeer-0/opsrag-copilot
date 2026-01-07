from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db import models

ROLE_ORDER = {"Viewer": 0, "Member": 1, "Admin": 2}


def require_role(db: Session, user_id: int, workspace_id: int, min_role: str):
    m = db.query(models.Membership).filter_by(user_id=user_id, workspace_id=workspace_id).first()
    if not m:
        raise HTTPException(status_code=403, detail="Not a member")
    if ROLE_ORDER.get(m.role, -1) < ROLE_ORDER.get(min_role, 0):
        raise HTTPException(status_code=403, detail="Insufficient role")
    return m
