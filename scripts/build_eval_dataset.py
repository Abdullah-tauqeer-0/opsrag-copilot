import json
from pathlib import Path

seed_dir = Path("corpus/seed")
out = Path("eval/datasets/qa_seed.jsonl")

items = []
for i, p in enumerate(sorted(seed_dir.glob("*.md"))):
    q = f"What is the key idea in {p.stem}?"
    items.append({"id": i, "question": q, "expected_doc": p.name})

full = []
while len(full) < 3060:
    for it in items:
        full.append(it)
        if len(full) >= 3060:
            break

out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", encoding="utf-8") as f:
    for it in full:
        f.write(json.dumps(it) + "\n")
