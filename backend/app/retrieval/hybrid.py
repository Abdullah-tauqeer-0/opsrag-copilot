from sqlalchemy import text


def hybrid_retrieve(db, workspace_id: int, query: str, k: int = 5, alpha: float = 0.6):
    lexical = db.execute(text("""
        SELECT c.id, d.title, c.text,
               ts_rank(to_tsvector('english', c.text), plainto_tsquery(:q)) AS score
        FROM chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE d.workspace_id = :ws
        ORDER BY score DESC
        LIMIT :k
    """), {"q": query, "ws": workspace_id, "k": k}).fetchall()

    vector = db.execute(text("""
        SELECT c.id, d.title, c.text,
               0.5 AS score
        FROM chunks c
        JOIN documents d ON d.id = c.document_id
        WHERE d.workspace_id = :ws
        LIMIT :k
    """), {"ws": workspace_id, "k": k}).fetchall()

    combined = {}
    for r in lexical:
        combined[r.id] = {"title": r.title, "text": r.text, "lex": float(r.score or 0), "vec": 0.0}
    for r in vector:
        if r.id not in combined:
            combined[r.id] = {"title": r.title, "text": r.text, "lex": 0.0, "vec": float(r.score or 0)}
        else:
            combined[r.id]["vec"] = float(r.score or 0)

    results = []
    for cid, data in combined.items():
        score = alpha * data["lex"] + (1 - alpha) * data["vec"]
        results.append({"chunk_id": cid, "title": data["title"], "text": data["text"], "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]
