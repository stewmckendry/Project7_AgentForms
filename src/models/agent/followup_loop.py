
from typing import Dict, Tuple
from src.models.llm_responsevalidators import llm_interpret_yes_no, llm_parse_date, llm_extract_symptoms
from src.models.llm_followups import generate_followup_question
from src.utils.logging.logger import setup_logger
logger = setup_logger()

PARSER_MAP = {
    "boolean": llm_interpret_yes_no,
    "date": llm_parse_date,
    "symptoms": llm_extract_symptoms,
    "text": lambda x: {
        "value": x.strip(),
        "certainty": "high" if x.strip() else "low",
        "thought": "Assumed correct as freeform text",
        "parsed_by": "text_default"
    }
}

def reparse_response(q_id: str, user_input: str, question_config: Dict) -> Dict:
    q_type = question_config[q_id].get("type", "text")
    parser = PARSER_MAP.get(q_type)
    if not parser:
        raise ValueError(f"No parser found for question type: {q_type}")
    return parser(user_input)

def run_followup_loop(finalized_responses: Dict, question_config: Dict) -> Tuple[Dict, Dict]:
    updated_responses = finalized_responses.copy()
    conversation_state = {}
    chat_log = {}

    for q_id, response in finalized_responses.items():
        prev_certainty = response.get("certainty", "low")
        if prev_certainty == "high":
            continue

        q_info = question_config.get(q_id)
        if not q_info:
            continue

        history = []
        retry_count = 0
        max_retries = 2

        while retry_count < max_retries:
            followup_data = generate_followup_question(q_id, response, q_info, conversation_state)
            followup_prompt = followup_data["followup_question"]
            reason = followup_data.get("reason", "Low certainty")

            print(f"💬 Follow-up ({q_id}): {followup_prompt}")
            print(f"🔍 Why: {reason}")
            user_input = input("👤 Your answer: ")

            if not user_input or user_input.strip().lower() in ["", "i don’t know", "idk"]:
                print("👋 Skipping question due to unclear or unknown response.")
                break

            parsed_response = reparse_response(q_id, user_input, question_config)
            new_certainty = parsed_response["certainty"]

            history.append({
                "input": user_input,
                "parsed_value": parsed_response["value"],
                "certainty": new_certainty,
                "thought": parsed_response.get("thought"),
                "parsed_by": parsed_response.get("parsed_by", "unknown")
            })

            if prev_certainty != "high" and new_certainty == "high":
                print(f"✅ Certainty improved from {prev_certainty} to high!")

            updated_responses[q_id] = parsed_response
            prev_certainty = new_certainty

            if new_certainty in ["medium", "high"]:
                break
            retry_count += 1

        conversation_state[q_id] = {
            "history": history,
            "final": updated_responses[q_id]
        }

        chat_log[q_id] = [q_info.get("prompt")] + [h["input"] for h in history]

    return updated_responses, conversation_state
