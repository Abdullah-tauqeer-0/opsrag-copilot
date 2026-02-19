import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.db import models
from backend.app.auth.security import hash_password
from backend.app.retrieval.chunking import chunk_text
from backend.app.retrieval.embeddings import EmbeddingProvider
from backend.app.db import models
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

for _ in range(30):
    try:
        engine.connect().close()
        break
    except Exception:
        time.sleep(1)

db = SessionLocal()

if not db.query(models.User).filter_by(email="admin@demo.local").first():
    admin = models.User(email="admin@demo.local", password_hash=hash_password("admin123"))
    member = models.User(email="member@demo.local", password_hash=hash_password("member123"))
    viewer = models.User(email="viewer@demo.local", password_hash=hash_password("viewer123"))
    db.add_all([admin, member, viewer])
    db.commit()

ws = db.query(models.Workspace).filter_by(name="Demo Workspace").first()
seed_dir = Path("corpus/seed")

existing = db.query(models.Document).filter_by(workspace_id=ws.id, source="seed").first()
if not existing and seed_dir.exists():
    embedder = EmbeddingProvider()
    for p in seed_dir.glob("*.md"):
        content = p.read_text(encoding="utf-8")
        doc = models.Document(workspace_id=ws.id, source="seed", title=p.name, status="uploaded")
        db.add(doc)
        db.commit()
        db.refresh(doc)
        chunks = chunk_text(content)
        vectors, model_name = embedder.embed(chunks)
        for idx, (text, vec) in enumerate(zip(chunks, vectors)):
            c = models.Chunk(document_id=doc.id, chunk_index=idx, text=text, metadata_json={})
            db.add(c)
            db.commit()
            e = models.Embedding(chunk_id=c.id, embedding=vec, model_name=model_name)
            db.add(e)
            db.commit()
        doc.status = "ready"
        db.commit()

    ws = models.Workspace(name="Demo Workspace")
    db.add(ws)
    db.commit()
    db.refresh(ws)

    db.add_all([
        models.Membership(user_id=admin.id, workspace_id=ws.id, role="Admin"),
        models.Membership(user_id=member.id, workspace_id=ws.id, role="Member"),
        models.Membership(user_id=viewer.id, workspace_id=ws.id, role="Viewer"),
    ])
    db.commit()

print("Demo ready:")
print("Backend: http://localhost:8000")
print("Frontend: http://localhost:3000")
print("Jaeger: http://localhost:16686")
print("Admin: admin@demo.local / admin123")
print("Member: member@demo.local / member123")
print("Viewer: viewer@demo.local / viewer123")
