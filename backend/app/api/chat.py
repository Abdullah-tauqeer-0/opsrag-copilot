from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.deps import get_current_user
from app.rbac.permissions import require_role
from app.db import models
from app.agents.agent import run_agent
from app.audit.logger import log_event

router = APIRouter()

@router.post("")
def chat(workspace_id: int, message: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    require_role(db, user.id, workspace_id, "Viewer")
    convo = models.Conversation(workspace_id=workspace_id, user_id=user.id)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    db.add(models.Message(conversation_id=convo.id, role="user", content=message))
    db.commit()
    log_event(db, workspace_id, user.id, "user_message", {"message": message})

    result = run_agent(db, workspace_id, message)
    log_event(db, workspace_id, user.id, "retrieval", {"citations": result.get("citations", [])})

    if result["mode"] == "proposal":
        approval = models.Approval(
            workspace_id=workspace_id,
            requested_by=user.id,
            status="pending",
            proposed_tool_calls_json=result["tool_calls"],
        )
        db.add(approval)
        db.commit()
        log_event(db, workspace_id, user.id, "tool_proposal", {"approval_id": approval.id, "tool_calls": result["tool_calls"]})
        return {"approval_request_id": approval.id, "citations": result["citations"]}

    db.add(models.Message(conversation_id=convo.id, role="assistant", content=result["answer"]))
    db.commit()
    log_event(db, workspace_id, user.id, "assistant_message", {"answer": result["answer"]})
    return {"answer": result["answer"], "citations": result["citations"]}

@router.get("/{conversation_id}")
def get_conversation(conversation_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    msgs = db.query(models.Message).filter_by(conversation_id=conversation_id).all()
    return [{"role": m.role, "content": m.content} for m in msgs]
