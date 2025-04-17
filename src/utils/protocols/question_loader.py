import yaml
from pathlib import Path

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed

def extract_question_list_from_yaml(yaml_path="data/protocols/concussion_assessment.yaml"):
    load_path = PROJECT_ROOT / yaml_path
    with open(load_path, "r") as f:
        data = yaml.safe_load(f)
    flow = data.get("stages", [])
    questions = []
    for stage in flow:
        for q in stage.get("questions", []):
            questions.append({
                "id": q["id"],
                "prompt": q["prompt"],
                "type": q.get("type", "text")
            })
    return questions
