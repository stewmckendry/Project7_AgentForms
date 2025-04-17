import yaml
from pathlib import Path
from src.utils.logging.logger import setup_logger
logger = setup_logger()

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed


def load_symptom_reference(path="data/protocols/symptoms_reference.yaml"):
    load_path = PROJECT_ROOT / path
    if not load_path.exists():
        logger.error(f"Concussion flow file not found at {load_path}")
        raise FileNotFoundError(f"Concussion flow file not found at {load_path}")
    logger.info(f"Loading concussion flow from {load_path}")
    with open(load_path, "r") as f:
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
