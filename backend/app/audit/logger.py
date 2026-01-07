from app.db import models

def log_event(db, workspace_id: int, user_id: int | None, event_type: str, payload: dict):
    entry = models.AuditLog(
        workspace_id=workspace_id,
        user_id=user_id,
        event_type=event_type,
        payload_json=payload,
    )
    db.add(entry)
    db.commit()
