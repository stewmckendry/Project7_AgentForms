# src/utils/protocols/load_question_strategy.py
import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_question_strategy(path: str = "data/protocols/concussion_questions.yaml") -> dict:
    """Load the follow-up question strategy config from YAML."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def extract_question_list_from_yaml(config: dict) -> list:
    return [
        {
            "id": qid,
            "prompt": entry.get("prompt", ""),
            "type": entry.get("type", "text"),
            "followup": entry.get("followup", {})
        }
        for qid, entry in config.items()
    ]
