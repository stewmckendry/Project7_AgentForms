from src.utils.protocols.question_loader import extract_question_list_from_yaml
from src.models.llm_responsevalidators import (
    llm_parse_date,
    llm_interpret_yes_no,
    llm_extract_symptoms
)
from src.utils.logging.logger import setup_logger
logger = setup_logger()

def finalize_draft_responses(agent):
    logger.info("Finalizing draft responses...")

    logger.info("Loading questions from flow...")
    qtype_lookup = {q["id"]: q["type"] for q in agent.known_questions}

    logger.info("Loading draft responses to questions from agent")
    draft_responses = agent.initial_analysis.get("draft_responses", {})

    logger.info("Processing each draft response...")
    for q_id, draft in draft_responses.items():
        qtype = qtype_lookup.get(q_id, "text")
        original_input = draft.get("value", "")
        thought_log = []

        # Record original draft
        thought_log.append({
            "source": "draft_inference",
            "value": original_input,
            "certainty": draft.get("certainty", "low"),
            "thought": draft.get("thought", "")
        })

        # Run the proper validator
        if qtype == "date":
            parsed = llm_parse_date(original_input)
            parsed_by = "llm_parse_date"
        elif qtype == "boolean":
            parsed = llm_interpret_yes_no(original_input)
            parsed_by = "llm_interpret_yes_no"
        elif qtype in ["list", "symptoms"]:
            parsed = llm_extract_symptoms(original_input)
            parsed_by = "llm_extract_symptoms"
        else:
            parsed = {
                "value": original_input,
                "certainty": draft.get("certainty", "low"),
                "thought": "No additional parsing applied.",
                "parsed_by": "draft_passthrough"
            }
            parsed_by = "draft_passthrough"

        # Add final parser result to log
        thought_log.append({
            "source": parsed_by,
            "value": parsed["value"],
            "certainty": parsed.get("certainty", "low"),
            "thought": parsed.get("thought", "")
        })

        # Store latest response + full history
        agent.responses[q_id] = {
            "value": parsed["value"],
            "certainty": parsed.get("certainty", "low"),
            "parsed_by": parsed_by,
            "thought": parsed.get("thought", ""),
            "history": thought_log,
            "original_input": parsed.get("original_input", original_input)
        }
