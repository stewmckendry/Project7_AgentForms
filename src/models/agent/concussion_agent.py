from src.utils.validation.response_validator import parse_date, parse_yes_no, parse_symptoms

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

    def get_next_question(self):
        if self.current_stage >= len(self.flow):
            return None
        stage = self.flow[self.current_stage]
        questions = stage["questions"]
        if self.current_question < len(questions):
            return questions[self.current_question]
        else:
            self.current_stage += 1
            self.current_question = 0
            return self.get_next_question()

    def record_response(self, question, answer):
        handler = QUESTION_HANDLERS.get(question)
        if handler:
            parsed = handler(answer)
            self.responses[question] = parsed
        else:
            self.responses[question] = answer
        self.current_question += 1

    def is_complete(self):
        return self.current_stage >= len(self.flow)

    def get_summary(self):
        return self.responses
