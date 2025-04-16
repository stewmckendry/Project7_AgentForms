import os
import json
from datetime import datetime
from pathlib import Path

# Get the project root (assumes this script is in src/ or notebooks/ folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # Adjust as needed

def export_json(responses):
    save_dir = PROJECT_ROOT / "outputs/returntoplay"
    save_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving JSON report to {save_dir}")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(save_dir, f"concussion_report_{ts}.json")
    with open(json_path, "w") as f:
        json.dump(responses, f, indent=2)
    return json_path


def export_markdown(chat_history, guidance):
    save_dir = PROJECT_ROOT / "outputs/returntoplay"
    save_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = os.path.join(save_dir, f"concussion_summary_{ts}.md")

    lines = ["# Concussion Session Report", ""]

    lines.append("## Conversation History\n")
    for speaker, msg in chat_history:
        prefix = "**You:**" if speaker == "👤" else "**Agent:**"
        lines.append(f"{prefix} {msg}")

    lines.append("\n## Return-to-Play Guidance\n")
    lines.append(guidance)

    with open(md_path, "w") as f:
        f.write("\n".join(lines))

    return md_path
