from datetime import datetime

def build_followup_trace_report(agent, followups):
    lines = []
    lines.append(f"# 🤖 Concussion Agent Follow-Up Trace Report")
    lines.append(f"Generated: {datetime.now().isoformat()}\n")
    lines.append("---\n")

    for f in followups:
        qid = f["id"]
        followup = f["followup"]
        reason = f["reason"]

        # Get the prompt from known_questions
        prompt = next((q["prompt"] for q in agent.known_questions if q["id"] == qid), "[Unknown prompt]")
        history = agent.responses.get(qid, {}).get("history", [])

        lines.append(f"## 🧩 Question ID: `{qid}`")
        lines.append(f"**Prompt:** {prompt}\n")

        lines.append(f"**Response History:**")
        for h in history:
            lines.append(f"- **{h['source']}** → Value: `{h['value']}` | Certainty: `{h['certainty']}`")
            if h.get("thought"):
                lines.append(f"  > {h['thought']}")

        lines.append(f"\n**💬 Follow-Up Question:** {followup}")
        lines.append(f"**📎 Reason:** {reason}")
        lines.append("\n---\n")

    return "\n".join(lines)
