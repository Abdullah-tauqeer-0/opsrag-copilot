from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from app.retrieval.hybrid import hybrid_retrieve

router = APIRouter()

@router.post("/debug")
def debug_retrieval(workspace_id: int, query: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Viewer")
    return hybrid_retrieve(db, workspace_id, query, k=10)
