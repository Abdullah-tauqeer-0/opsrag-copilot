from worker.worker import celery
from backend.app.db.session import SessionLocal
from backend.app.db import models
from backend.app.retrieval.chunking import chunk_text
from backend.app.retrieval.embeddings import EmbeddingProvider

@celery.task
def ingest_document(doc_id: int, content: str):
    db = SessionLocal()
    try:
        doc = db.query(models.Document).filter_by(id=doc_id).first()
        if not doc:
            return
        doc.status = "processing"
        db.commit()
        chunks = chunk_text(content)
        embedder = EmbeddingProvider()
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
    finally:
        db.close()
