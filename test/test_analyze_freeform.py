# test_analyze_freeform.py
import re
from src.models.llm_analyze_freeform_input import analyze_freeform_input
from src.models.agent.concussion_agent import ConcussionAgent

def test_analyze_freeform_input_soft():
    agent = ConcussionAgent()
    user_input = "My son hit his head during practice yesterday and felt dizzy afterwards."
    result = analyze_freeform_input(agent, user_input)

    assert "draft_responses" in result
    assert isinstance(result["draft_responses"], dict)
    assert "summary_thought" in result

    injury = result["draft_responses"].get("injury_date")
    if injury:
        value = injury.get("value")
        if isinstance(value, str):
            assert re.match(r"^\d{4}-\d{2}-\d{2}$", value), f"Injury date not in yyyy-mm-dd format: {value}"

    print("Soft validation complete: draft_responses, summary_thought, and injury_date format OK")
