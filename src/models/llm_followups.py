from src.models.llm_openai import call_openai_chat
from src.utils.logging.logger import setup_logger
logger = setup_logger()

def generate_followup_question(q_id, response, strategy_entry, all_responses=None):
    """
    Generate a follow-up question using the response, strategy entry, and optionally other context.

    Args:
        q_id (str): The question ID (e.g., 'injury_date')
        response (dict): Finalized response for this question
        strategy_entry (dict): Info from question_strategy.yaml
        all_responses (dict): All finalized responses (optional)

    Returns:
        dict: {
            question_id,
            followup_question,
            reason,
            importance
        }
    """
    logger.info(f"Generating follow-up question for {q_id}...")
    
    value = response.get("value")
    certainty = response.get("certainty", "low")
    thought = response.get("thought", "")
    prompt = strategy_entry.get("prompt", "")
    intent = strategy_entry.get("intent", "")
    mode = strategy_entry.get("mode", "clarify")
    q_type = strategy_entry.get("type", "text")
    example_fups = strategy_entry.get("followup_ideas", [])

    context_summary = ""
    if all_responses:
        context_lines = []
        for other_qid, resp in all_responses.items():
            if other_qid != q_id and resp.get("value") not in [None, "", []]:
                val = resp.get("value")
                if isinstance(val, list):
                    val = ", ".join(val)
                context_lines.append(f"- {other_qid}: {val}")
        context_summary = "\n".join(context_lines)

    system_prompt = (
        "You are an assistant helping generate intelligent follow-up questions during a concussion assessment.\n"
        "You are given a partially answered question and its context.\n\n"
        f"Question prompt: {prompt}\n"
        f"Question type: {q_type}\n"
        f"Intent: {intent}\n"
        f"Follow-up mode: {mode}\n"
        f"Existing answer: {value}\n"
        f"Certainty: {certainty}\n"
        f"Thought: {thought}\n"
    )

    if example_fups:
        system_prompt += f"Example follow-ups: {', '.join(example_fups)}\n"

    if context_summary:
        system_prompt += f"\nOther known info:\n{context_summary}\n"

    system_prompt += (
        "\nGenerate a short, natural follow-up question that either clarifies or probes further. "
        "Then explain briefly why this question is important.\n"
        "Return both on separate lines. No markdown."
    )

    user_prompt = f"Please generate a follow-up for question ID '{q_id}'"

    raw = call_openai_chat(system_prompt, user_prompt)
    lines = raw.strip().split("\n")
    return {
        "question_id": q_id,
        "followup_question": lines[0].strip(),
        "reason": " ".join(lines[1:]).strip(),
        "importance": "high" if certainty == "low" else "medium"
    }
