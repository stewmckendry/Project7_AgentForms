import re
import json

def repair_json_like_string(s: str) -> str:
    """
    Cleans LLM output to make it safe for json.loads().
    - Removes markdown code fences
    - Fixes trailing commas
    - Converts single quotes to double quotes
    - Normalizes true/false/null
    """
    s = s.strip()

    # Remove markdown fences (``` or ```json)
    s = re.sub(r"^```(?:json)?", "", s, flags=re.IGNORECASE | re.MULTILINE)
    s = re.sub(r"```$", "", s.strip(), flags=re.MULTILINE)

    # Remove trailing commas before } or ]
    s = re.sub(r",\s*(?=[}\]])", "", s)

    # Convert single quotes to double quotes (but not inside strings)
    s = re.sub(r"(?<!\\)'", '"', s)

    # Normalize true/false/null for JSON
    s = re.sub(r'\bTrue\b', 'true', s)
    s = re.sub(r'\bFalse\b', 'false', s)
    s = re.sub(r'\bNone\b', 'null', s)

    return s

# Example usage
# safe_json = json.loads(repair_json_like_string(llm_response))


def repair_yaml_like_string(s: str) -> str:
    import re
    # Remove code fences or extraneous indentation
    s = s.strip()
    s = re.sub(r"^```(?:yaml|yml)?", "", s, flags=re.IGNORECASE | re.MULTILINE)
    s = re.sub(r"```$", "", s, flags=re.MULTILINE)
    return s.strip()