"""Journalisation des résultats VERITAS."""

import json
import hashlib
from datetime import datetime

LOG_FILE = ".veritas_outcomes.jsonl"


def log_outcome(prompt: str, pipeline: dict) -> None:
    """Journalisation minimale, aucun effet sur le routage.
    ground_truth_mode reste vide : à annoter a posteriori (condition #3)."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:8],
        "prompt_snippet": prompt[:100].replace("\n", " "),
        "mode_predicted": pipeline["mode"],
        "constraints_applied": pipeline["constraints_applied"],
        "ground_truth_mode": None,   # à remplir manuellement après relecture
        "was_correct": None,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
