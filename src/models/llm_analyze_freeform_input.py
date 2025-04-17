# Updated src/models/llm_analyze_freeform_input.py
from src.utils.protocols.load_symptom_reference import load_symptom_reference
from src.models.llm_responsevalidators import llm_extract_symptoms, llm_interpret_yes_no, llm_parse_date
from src.models.llm_openai import call_openai_chat
from src.utils.processing.json_yaml_repair import repair_yaml_like_string
import yaml

def run_llm_draft_extraction(agent: str, user_input: str, known_questions: list) -> dict:
    system_prompt = (
        "You are an AI reasoning assistant helping to assess a possible concussion based on a free-form explanation.\n"
        "You will be given:\n"
        "1. A description of the situation from a coach or parent\n"
        "2. A list of structured assessment questions\n\n"
        "Your job is to:\n"
        "- Try to answer each question based on what the user wrote\n"
        "- For each, include:\n"
        "   value: your best answer (can be text, boolean, number, date, or list)\n"
        "   certainty: high / medium / low\n"
        "   thought: how you arrived at that answer\n"
        "- If a question can't be answered, set value: null and certainty: low\n"
        "- At the end, include a summary_thought with your overall interpretation of the situation\n\n"
        "Output format:\n"
        "draft_responses:\n"
        "  question_id_1:\n"
        "    value: ...\n"
        "    certainty: ...\n"
        "    thought: ...\n"
        "    parsed_by: LLM-Free Form Triage\n"
        "  question_id_2:\n"
        "    ...\n"
        "summary_thought: ...\n\n"
        "**IMPORTANT** Return your answer as valid YAML. No markdown fences. No extra commentary. Just the YAML block."
    )

    user_prompt = f"""
free_text: "{user_input}"
questions:
  - {chr(10).join([q['id'] for q in known_questions])}
"""

    raw_output = call_openai_chat(system_prompt, user_prompt, model="gpt-4", temperature=0.3)
    yaml_str = repair_yaml_like_string(raw_output)
    return yaml.safe_load(yaml_str)

def analyze_freeform_input(agent: str, user_input: str) -> dict:
    """
    Analyze a free-form explanation and attempt to answer known assessment questions.

    Parameters:
        agent (str): identifier for agent version or strategy
        user_input (str): the full narrative or situation description
        known_questions (list of dict): list of known questions with ids and types

    Returns:
        dict with keys:
            - 'draft_responses': dict of question_id -> {value, thought, certainty, parsed_by}
            - 'summary_thought': overall summary string
    """
    known_questions = getattr(agent, 'known_questions', [])
    if not known_questions:
        return {"draft_responses": {}, "summary_thought": "No questions available in agent."}

    symptom_ref = load_symptom_reference("data/protocols/symptoms_reference.yaml")
    llm_result = run_llm_draft_extraction(agent, user_input, known_questions)
    llm_draft = llm_result.get("draft_responses", {})
    summary = llm_result.get("summary_thought", "")

    draft_responses = {}

    for q in known_questions:
        qid = q["id"]
        qtype = q.get("type", "text")
        raw = llm_draft.get(qid, {})
        parsed = {"value": raw.get("value"), "thought": raw.get("thought", ""), "certainty": raw.get("certainty", "low"), "parsed_by": "LLM-Free Form Triage"}

        if qtype == "symptoms":
            parsed = llm_extract_symptoms(user_input, symptom_ref)
        elif qtype == "boolean":
            parsed = llm_interpret_yes_no(user_input)
        elif qtype == "date":
            parsed = llm_parse_date(user_input)

        draft_responses[qid] = parsed

    return {
        "draft_responses": draft_responses,
        "summary_thought": summary
    }
