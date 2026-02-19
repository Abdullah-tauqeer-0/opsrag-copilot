from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role

router = APIRouter()

@router.get("")
def list_workspaces(db: Session = Depends(get_db), user=Depends(get_current_user)):
    ws = db.query(models.Workspace).join(models.Membership, models.Membership.workspace_id == models.Workspace.id).filter(models.Membership.user_id == user.id).all()
    return [{"id": w.id, "name": w.name} for w in ws]

@router.post("")
def create_workspace(name: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    w = models.Workspace(name=name)
    db.add(w)
    db.commit()
    db.refresh(w)
    db.add(models.Membership(user_id=user.id, workspace_id=w.id, role="Admin"))
    db.commit()
    return {"id": w.id, "name": w.name}

@router.post("/{id}/members")
def add_member(id: int, user_id: int, role: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, id, "Admin")
    db.add(models.Membership(user_id=user_id, workspace_id=id, role=role))
    db.commit()
    return {"ok": True}

@router.patch("/{id}/members/{user_id}")
def update_member(id: int, user_id: int, role: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, id, "Admin")
    m = db.query(models.Membership).filter_by(user_id=user_id, workspace_id=id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Not found")
    m.role = role
    db.commit()
    return {"ok": True}
