from src.utils.protocols.question_loader import extract_question_list_from_yaml
from src.models.llm_responsevalidators import (
    llm_parse_date,
    llm_interpret_yes_no,
    llm_extract_symptoms
)
from src.utils.protocols.load_symptom_reference import load_symptom_reference
from src.utils.logging.logger import setup_logger
logger = setup_logger()

def finalize_draft_responses(agent, symptom_reference=None):
    logger.info("Finalizing draft responses...")

    logger.info("Loading questions from flow...")
    qtype_lookup = {q["id"]: q["type"] for q in agent.known_questions}

    logger.info("Loading draft responses to questions from agent's initial analysis...")
    draft_responses = agent.initial_analysis.get("draft_responses", {})

    logger.info("Loading clinical symptoms reference...")
    if not symptom_reference:
        symptom_reference = load_symptom_reference()

    finalized = {}

    logger.info("Processing each draft response with a validator..")
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
            logger.info(f"Parsing date for question {q_id}...")
            parsed = llm_parse_date(original_input)
            parsed_by = "llm_parse_date"
        elif qtype == "boolean":
            logger.info(f"Parsing boolean for question {q_id}...")
            parsed = llm_interpret_yes_no(original_input)
            parsed_by = "llm_interpret_yes_no"
        elif qtype in ["list", "symptoms"]:
            logger.info(f"Extracting symptoms for question {q_id}...")
            parsed = llm_extract_symptoms(original_input, symptom_reference=symptom_reference)
            parsed["certainty"] = draft.get("certainty", parsed.get("certainty"))
            parsed["thought"] = draft.get("thought", parsed.get("thought"))
            parsed["original_input"] = original_input
            parsed_by = "llm_extract_symptoms"
            finalized[q_id] = parsed
        else:
            logger.info(f"Passing through value for question {q_id}...")
            parsed = {
                "value": original_input,
                "certainty": draft.get("certainty", "low"),
                "thought": "No additional parsing applied.",
                "parsed_by": "draft_passthrough"
            }
            parsed_by = "draft_passthrough"

        # Add final parser result to log
        logger.info(f"Parsed result for question {q_id}: {parsed}")
        logger.info("Adding parsed result to thought log...")
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
        logger.info(f"Stored final response for question {q_id}: {agent.responses[q_id]}")
