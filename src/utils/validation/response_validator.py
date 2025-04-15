from dateutil import parser
import re

YES_WORDS = {"yes", "y", "yeah", "yep", "sure", "true"}
NO_WORDS = {"no", "n", "nope", "nah", "false"}

def parse_date(text):
    try:
        dt = parser.parse(text, fuzzy=True)
        return dt.date().isoformat()
    except Exception:
        return None

def parse_yes_no(text):
    lowered = text.lower()
    if lowered in YES_WORDS:
        return True
    if lowered in NO_WORDS:
        return False
    return None

def parse_symptoms(text):
    # Naive matcher — can evolve into NLP-based version later
    symptoms = [
        "headache", "dizziness", "blurred vision", "nausea",
        "confusion", "sensitivity to light", "balance problems",
        "memory loss", "ringing in ears", "fatigue"
    ]
    found = [s for s in symptoms if s in text.lower()]
    return found
