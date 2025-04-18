# src/utils/protocols/load_symptom_reference.py
import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_symptom_reference(path: str = "data/protocols/symptoms_reference.yaml") -> dict:
    """Load the symptom reference YAML used to enrich symptom values."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def match_symptoms(user_symptoms, reference):
    matched = []
    for symptom in user_symptoms:
        for ref in reference:
            if symptom.lower() in [ref["name"].lower()] + ref.get("aliases", []):
                matched.append({
                    "name": ref["name"],
                    "severity": ref["severity"],
                    "category": ref["category"],
                    "flags": ref.get("flags", []),
                })
                break
    return matched
