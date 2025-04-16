from datetime import date, datetime
from src.models.llm_openai import call_openai_chat
from src.utils.logging.logger import setup_logger
logger = setup_logger()


def llm_parse_date(input_text):
    logger.info(f"Parsing date with LLM for input: {input_text}")

    today = date.today().isoformat()

    system_prompt = (
        f"You are an assistant that extracts precise or estimated calendar dates from user input.\n"
        f"Today’s date is {today}. If the user says things like 'last Friday' or 'this morning', "
        f"interpret it relative to today's date. Return the result in YYYY-MM-DD format.\n"
        f"First, explain your reasoning.\n"
        f"Then, on the final line, output:\n"
        f"      date: <YYYY-MM-DD|null> | certainty: <high|medium|low>\n"
        f"If the date is vague but guessable (e.g., 'early April'), return your best estimated date in the YYYY-MM-DD format. \n"
        f"If no date can be inferred, write 'null' for date.\n"
    )

    user_prompt = f"The user said: {input_text}"
    llm_response = call_openai_chat(system_prompt, user_prompt)
    lines = llm_response.strip().splitlines()

    # Default values
    value = "null"
    certainty = "low"
    thought = ""

    if lines:
        # Try to parse last line: "date: 2025-04-15 | certainty: high"
        last_line = lines[-1].lower().strip()
        if "date:" in last_line and "certainty:" in last_line:
            try:
                parts = [part.strip() for part in last_line.replace("date:", "").split("|")]
                value = parts[0]
                certainty = parts[1].replace("certainty:", "").strip()
                thought = "\n".join(lines[:-1]).strip()
            except Exception:
                thought = "\n".join(lines).strip()
        else:
            thought = llm_response.strip()
    
    # Fallbacks if something went wrong or symptoms/certainty is missing
    if not certainty or certainty not in {"low", "medium", "high"}:
        certainty = "low"

    logger.info(f"Parsed date: {value}, Certainty: {certainty}, Thought: {thought}")

    return {
        "value": value,
        "certainty": certainty,
        "parsed_by": "llm",
        "original_input": input_text,
        "thought": thought
    }

def llm_interpret_yes_no(input_text):
    logger.info(f"Interpreting yes/no response with LLM for input: {input_text}")
    system_prompt = (
            "You are a reasoning assistant that classifies yes/no responses. Your job is to:\n"
            "1. Interpret the user's intent as one of:\n"
            "   - 'yes' → if there's a clear or even partial leaning toward agreement\n"
            "   - 'no' → only if the user explicitly expresses disagreement or denial\n"
            "   - 'partial' → if the user qualifies the answer (e.g. 'yes, but only for a bit')\n"
            "   - 'uncertain' → if the user doesn’t know, avoids answering, or the information is missing\n"
            "   Important clarification:\n"
            "   - If the user says 'they didn't mention it' or anything similar, do NOT assume that means 'no'.\n"
            "   - This indicates missing information — classify it as 'uncertain'.\n"
            "2. Estimate how confident the user sounds: high, medium, or low certainty.\n"
            "3. First, explain your reasoning.\n"
            "4. Then, on the last line, output:\n"
            "   intent: <yes|no|partial|uncertain> | certainty: <high|medium|low>\n"
            "\n"
            "Examples:\n"
            "Input: 'absolutely' → intent: yes | certainty: high\n"
            "Input: 'I guess so' → intent: yes | certainty: medium\n"
            "Input: 'no, he was fine' → intent: no | certainty: high\n"
            "Input: 'I'm not sure, maybe' → intent: uncertain | certainty: low"
        )

    user_prompt = f"The user said: {input_text}"
    llm_interpret_yes_no_response = call_openai_chat(system_prompt, user_prompt)
    lines = llm_interpret_yes_no_response.splitlines()
    thought = ""
    intent = "uncertain"
    certainty = "low"

    if lines:
        if "intent:" in lines[-1].lower():
            try:
                # Parse final line
                last_line = lines[-1].lower().replace("intent:", "").strip()
                parts = [part.strip() for part in last_line.split("|")]
                if len(parts) == 2:
                    intent = parts[0]
                    certainty = parts[1].replace("certainty:", "").strip()
                thought = "\n".join(lines[:-1]).strip()
            except Exception:
                pass
        else:
            thought = "\n".join(lines).strip()

    logger.info(f"Parsed intent: {intent}, Certainty: {certainty}, Thought: {thought}")

    # Fallbacks if something went wrong or symptoms/certainty is missing
    if not certainty or certainty not in {"low", "medium", "high"}:
        certainty = "low"

    return {
        "value": intent,
        "certainty": certainty,
        "parsed_by": "llm",
        "original_input": input_text,
        "thought": thought
    }

def llm_extract_symptoms(input_text):

    logger.info(f"Extracting symptoms with LLM for input: {input_text}")

    system_prompt = (
        "You are a helpful assistant trained to identify concussion symptoms from a user's input.\n"
        "\n"
        "Your task:\n"
        "1. Extract any symptoms described, using clear terms like: headache, dizziness, nausea, confusion, blurry vision, sensitivity to light, etc.\n"
        "2. Estimate how confident you are in your extraction: high, medium, or low.\n"
        "3. First, explain your reasoning.\n"
        "4. Then, on the final line, output:\n"
        "   symptoms: [comma-separated list] | certainty: <high|medium|low>\n"
        "\n"
        "Examples:\n"
        "Input: 'He had a headache and felt dizzy' → symptoms: [headache, dizziness] | certainty: high\n"
        "Input: 'She just seemed a bit off' → symptoms: [] | certainty: low"
    )

    user_prompt = f"The user said: {input_text}"
    llm_response = call_openai_chat(system_prompt, user_prompt)
    lines = llm_response.strip().splitlines()

    symptoms = []
    certainty = "low"
    thought = ""

    if lines:
        last_line = lines[-1].lower().strip()
        if "symptoms:" in last_line and "certainty:" in last_line:
            try:
                parts = last_line.replace("symptoms:", "").split("|")
                symptoms_part = parts[0].strip()
                certainty = parts[1].replace("certainty:", "").strip()

                # Parse symptom list from string
                symptoms = [s.strip() for s in symptoms_part.strip("[]").split(",") if s.strip()]
                thought = "\n".join(lines[:-1]).strip()
            except Exception:
                thought = llm_response.strip()
        else:
            thought = llm_response.strip()
    
    # Fallbacks if something went wrong or symptoms/certainty is missing
    if not isinstance(symptoms, list):
        symptoms = []
    if not certainty or certainty not in {"low", "medium", "high"}:
        certainty = "low"
    
    logger.info(f"Parsed symptoms: {symptoms}, Certainty: {certainty}, Thought: {thought}")

    return {
        "value": symptoms,
        "certainty": certainty,
        "parsed_by": "llm",
        "original_input": input_text,
        "thought": thought
    }

def parse_with_fallback(input_text, type_hint):
    try:
        if type_hint == "date":
            return llm_parse_date(input_text)
        elif type_hint == "boolean":
            return llm_interpret_yes_no(input_text)
        elif type_hint == "list":
            return llm_extract_symptoms(input_text)
        else:
            return {"value": input_text, "parsed_by": "raw"}
    except Exception as e:
        return {"value": input_text, "parsed_by": "error", "error": str(e)}


def is_valid_date_string(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False