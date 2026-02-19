import os
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

LOCAL_EMBED_DIM = int(os.getenv("LOCAL_EMBED_DIM", "384"))


class EmbeddingProvider:
    def __init__(self):
        self.use_local = os.getenv("USE_LOCAL_EMBEDDINGS", "1") == "1"
        self.model = None
        if self.use_local and SentenceTransformer:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception:
                self.model = None

    def embed(self, texts):
        if self.model:
            return self.model.encode(texts).tolist(), "all-MiniLM-L6-v2"
        vecs = []
        for t in texts:
            h = np.zeros(LOCAL_EMBED_DIM, dtype=np.float32)
            for i, ch in enumerate(t.encode("utf-8")):
                h[i % LOCAL_EMBED_DIM] += (ch % 31) / 31.0
            norm = np.linalg.norm(h) + 1e-8
            vecs.append((h / norm).tolist())
        return vecs, "hash-embed-v1"
