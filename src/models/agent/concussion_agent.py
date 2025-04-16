from src.utils.validation.response_validator import parse_date, parse_yes_no, parse_symptoms
from src.models.llm_responsevalidators import llm_parse_date, llm_interpret_yes_no, llm_extract_symptoms
from src.models.llm_analyze_freeform_input import analyze_freeform_input
from src.utils.logging.logger import setup_logger
logger = setup_logger()
logger.info("Concussion agent started")

QUESTION_HANDLERS = {
    "When did the injury occur?": parse_date,
    "Did the player lose consciousness?": parse_yes_no,
    "What symptoms did the player experience after the incident?": parse_symptoms,
    "Has the player been seen by a healthcare provider?": parse_yes_no,
    "Have they been officially diagnosed with a concussion?": parse_yes_no,
    "Is the player still experiencing symptoms?": parse_yes_no,
    "Has the player been cleared to return to play by a professional?": parse_yes_no
}

class ConcussionAgent:
    def __init__(self, flow):
        self.flow = flow
        self.responses = {}
        self.current_stage = 0
        self.current_question = 0
        self.free_text = None
        self.initial_analysis = None

    def get_next_question(self):
        if self.current_stage >= len(self.flow):
            return None
        stage = self.flow[self.current_stage]
        questions = stage["questions"]
        if self.current_question < len(questions):
            logger.info(f"Current question: {questions[self.current_question]['prompt']}, Stage: {self.current_stage} of {len(self.flow)}, Question: {self.current_question}")
            return questions[self.current_question]["prompt"]
        else:
            self.current_stage += 1
            self.current_question = 0
            logger.info(f"Moving to the next stage. Current stage: {self.current_stage} of {len(self.flow)}, Question: {self.current_question}")
            return self.get_next_question()

    def record_response(self, question_prompt, answer):
        # Find question config by prompt
        question_config = None
        for stage in self.flow:
            for q in stage["questions"]:
                if q["prompt"] == question_prompt:
                    question_config = q
                    break

        if not question_config:
            return

        qid = question_config["id"]
        qtype = question_config.get("type")
        parser = question_config.get("parse_with")

        # Use LLM validator based on type or parser hint
        if parser == "symptom_extractor" or qtype == "list":
            logger.info(f"Parsing symptoms with LLM for question: {qid}")
            parsed = llm_extract_symptoms(answer)
            logger.info(f"Parsed symptoms: {parsed}")
        elif qtype == "date":
            logger.info(f"Parsing date with LLM for question: {qid}")
            parsed = llm_parse_date(answer)
            logger.info(f"Parsed date: {parsed}")
        elif qtype == "boolean":
            logger.info(f"Parsing boolean with LLM for question: {qid}")
            parsed = llm_interpret_yes_no(answer)
            logger.info(f"Parsed boolean: {parsed}")
        else:
            logger.info(f"Recording raw answer for question: {qid}")
            parsed = {"value": answer, "parsed_by": "raw"}
            logger.info(f"Raw answer: {parsed}")

        self.responses[qid] = parsed
        self.current_question += 1

    def is_complete(self):
        return self.current_stage >= len(self.flow)

    def get_summary(self):
        return {
            "responses": self.responses,
            "free_text": getattr(self, "free_text", ""),
            "summary_thought": getattr(self, "initial_analysis", {}).get("summary_thought", ""),
            "stage_completed": self.current_stage
        }

    def record_freeform_analysis(self, user_input):
        
        self.free_text = user_input

        # Run LLM analysis on the free-form input
        result = analyze_freeform_input(user_input)

        self.initial_analysis = {
            "free_text": user_input,
            "draft_responses": result.get("draft_responses", {}),
            "summary_thought": result.get("summary_thought", ""),
        }

        # Optionally preload any confident answers into self.responses
        for q_id, info in result.get("draft_responses", {}).items():
            if info.get("certainty") == "high" and info.get("value") not in [None, ""]:
                self.responses[q_id] = {
                    "value": info["value"],
                    "certainty": info["certainty"],
                    "thought": info.get("thought", ""),
                    "parsed_by": "llm_draft"
                }