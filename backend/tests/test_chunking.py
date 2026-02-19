from app.retrieval.chunking import chunk_text

def test_chunking():
    chunks = chunk_text("a " * 1000)
    assert len(chunks) > 1
