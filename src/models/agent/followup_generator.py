from src.utils.protocols.load_question_strategy import load_question_strategy
from src.models.llm_followups import generate_followup_question
from src.utils.logging.logger import setup_logger
logger = setup_logger()


def generate_followups_from_responses(finalized_responses, strategy_path="data/protocols/question_strategy.yaml"):
    """
    Generate follow-up questions based on finalized responses using strategy config.

    Args:
        finalized_responses (dict): Final output from finalize_draft_responses
        strategy_path (str): Path to question_strategy.yaml

    Returns:
        list of follow-up dicts with question_id, followup_question, reason, importance
    """
    strategy = load_question_strategy(strategy_path)
    followups = []

    for q_id, response in finalized_responses.items():
        if response.get("certainty") != "high":
            strat_entry = next((s for s in strategy if s["id"] == q_id), None)
            if strat_entry:
                try:
                    fup = generate_followup_question(
                        q_id=q_id,
                        response=response,
                        strategy_entry=strat_entry,
                        all_responses=finalized_responses
                    )
                    followups.append(fup)
                except Exception as e:
                    print(f"[⚠️] Error generating follow-up for {q_id}: {e}")

    return followups

