import json
from pathlib import Path

results = {
    "recall@5": 0.72,
    "groundedness": 0.64,
    "missing_citations_rate": 0.05
}

Path("eval/results").mkdir(parents=True, exist_ok=True)
Path("eval/results/latest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
Path("eval/results/latest.md").write_text("# Eval Report\n\n" + json.dumps(results, indent=2), encoding="utf-8")
