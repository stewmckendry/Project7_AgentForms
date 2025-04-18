# src/utils/protocols/load_concussion_flow.py
import yaml
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_concussion_flow(path: str = "data/protocols/concussion_assessment.yaml") -> list:
    """Load the concussion assessment flow YAML as a list of questions."""
    with open(path, "r") as f:
        return yaml.safe_load(f)
