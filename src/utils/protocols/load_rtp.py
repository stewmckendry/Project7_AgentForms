# src/utils/protocols/load_rtp.py
import yaml
from pathlib import Path
from functools import lru_cache

def get_rtp_path() -> Path:
    return Path("data/protocols/return_to_play.yaml")

@lru_cache(maxsize=1)
def load_return_to_play_protocol() -> list:
    """Load the return-to-play protocol YAML as a list of stage dictionaries."""
    path = get_rtp_path()
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data
