import os, requests
from pathlib import Path

RAW = Path("corpus/raw")
PROCESSED = Path("corpus/processed")
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

URLS = [
    "https://nvlpubs.nist.gov/nistpubs/AI/NIST.AI.100-1.pdf",
    "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
    "https://airc.nist.gov/airmf-resources/playbook/",
]

for url in URLS:
    name = url.split("/")[-1] or "playbook.html"
    path = RAW / name
    if not path.exists():
        r = requests.get(url)
        path.write_bytes(r.content)

for p in RAW.iterdir():
    text = p.read_text(errors="ignore")
    (PROCESSED / f"{p.stem}.md").write_text(text[:5000], encoding="utf-8")
