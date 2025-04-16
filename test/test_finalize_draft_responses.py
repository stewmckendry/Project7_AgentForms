import pytest
from unittest.mock import patch
from src.models.agent.concussion_agent import ConcussionAgent
from src.utils.processing.process_draft_response import finalize_draft_responses
from src.utils.protocols.load_concussion_flow import load_concussion_flow

@pytest.fixture
def mock_agent():
    CONCUSSION_FLOW = load_concussion_flow("data/protocols/concussion_flow.yaml")
    agent = ConcussionAgent()
    agent.initial_analysis = {
        "draft_responses": {
            "injury_date": {
                "value": "yesterday",
                "certainty": "high",
                "thought": "User mentioned it happened yesterday."
            },
            "symptoms": {
                "value": "headache, dizziness",
                "certainty": "medium",
                "thought": "Mentioned symptoms casually."
            }
        }
    }
    return agent

@patch("src.models.llm_responsevalidators.llm_parse_date")
@patch("src.models.llm_responsevalidators.llm_extract_symptoms")
@patch("src.utils.protocols.question_loader.extract_question_list_from_yaml")
def test_finalize_responses_with_parsers(
    mock_extract_questions, mock_symptom_parser, mock_date_parser, mock_agent
):
    mock_extract_questions.return_value = [
        {"id": "injury_date", "prompt": "...", "type": "date"},
        {"id": "symptoms", "prompt": "...", "type": "symptoms"},
    ]

    mock_date_parser.return_value = {
        "value": "2025-04-15",
        "certainty": "high",
        "thought": "Parsed relative to today",
        "original_input": "yesterday"
    }

    mock_symptom_parser.return_value = {
        "value": ["headache", "dizziness"],
        "certainty": "high",
        "thought": "Mapped common terms",
        "original_input": "headache, dizziness"
    }

    finalize_draft_responses(mock_agent)

    assert "injury_date" in mock_agent.responses
    assert mock_agent.responses["injury_date"]["value"] == "2025-04-15"
    assert mock_agent.responses["injury_date"]["parsed_by"] == "llm_parse_date"
    assert len(mock_agent.responses["injury_date"]["history"]) == 2

    assert mock_agent.responses["symptoms"]["value"] == ["headache", "dizziness"]
    assert mock_agent.responses["symptoms"]["certainty"] == "high"
