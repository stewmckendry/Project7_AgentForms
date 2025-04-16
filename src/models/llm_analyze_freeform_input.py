import json
from src.models.llm_openai import call_openai_chat
from src.utils.protocols.question_loader import extract_question_list_from_yaml
from src.utils.logging.logger import setup_logger
logger = setup_logger()

def analyze_freeform_input(agent, user_input):
    '''
    Analyze a free-form explanation and attempt to answer known assessment questions.

    Parameters:
    - user_input (str): the full narrative or situation description
    - known_questions (list of dict): each with {id, prompt, type}

    Returns:
    - dict with keys:
        - 'draft_responses': dict keyed by question_id with {value, thought, certainty, parsed_by}
        - 'summary_thought': overall explanation of what was extracted
    '''
    logger.info("Calling LLM to analyze free-form input & map to questions for concussion assessment")
    questions = agent.known_questions
    system_prompt = (
        "You are an AI reasoning assistant helping to assess a possible concussion based on a free-form explanation.\n"
        "You will be given:\n"
        "1. A description of the situation from a coach or parent\n"
        "2. A list of structured assessment questions\n\n"
        "Your job is to:\n"
        "- Try to answer each question based on what the user wrote\n"
        "- For each, include:\n"
        "   * value: your best answer\n"
        "   * certainty: high / medium / low\n"
        "   * thought: how you arrived at that answer\n"
        "- If a question can't be answered, leave value null and certainty low\n"
        "- At the end, include a 'summary_thought' with your overall interpretation\n\n"
        "Output format:\n"
        "{\n"
        "  \"draft_responses\": {\n"
        "    \"question_id_1\": {\"value\": ..., \"certainty\": ..., \"thought\": ...},\n"
        "    \"question_id_2\": {...},\n"
        "    ...\n"
        "  },\n"
        "  \"summary_thought\": \"...\"\n"
        "}\n"
    )

    question_list_text = "\n".join(
        [f"- {q['id']}: {q['prompt']}" for q in questions]
    )

    user_prompt = (
        f"The user said:\n\"\"\"\n{user_input.strip()}\n\"\"\"\n\n"
        f"The assessment questions are:\n{question_list_text}"
    )

    llm_response = call_openai_chat(system_prompt, user_prompt)

    try:
        parsed = json.loads(llm_response)
        return parsed
    except Exception:
        return {
            "draft_responses": {},
            "summary_thought": "Could not parse structured output from LLM.",
            "raw_llm_response": llm_response
        }
