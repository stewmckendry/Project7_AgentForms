import yaml
from pathlib import Path
from src.utils.logging.logger import setup_logger
logger = setup_logger()
logger.info("Concussion flow loading started")

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed


def load_question_strategy(path="data/protocols/question_strategy.yaml"):
    load_path = PROJECT_ROOT / path
    if not load_path.exists():
        logger.error(f"Concussion flow file not found at {load_path}")
        raise FileNotFoundError(f"Concussion flow file not found at {load_path}")
    logger.info(f"Loading concussion flow from {load_path}")    
    with open(load_path, "r") as f:
        return yaml.safe_load(f)
