import pytest
from src.models.agent.concussion_agent import ConcussionAgent
from src.utils.protocols.load_concussion_flow import load_concussion_flow

@pytest.fixture
def sample_agent():
    flow = load_concussion_flow()
    return ConcussionAgent(flow)

def test_agent_runs_to_completion(sample_agent):
    agent = sample_agent
    q_count = 0
    while True:
        q = agent.get_next_question()
        if q is None:
            break
        agent.record_response(q["prompt"], "test input")  # Use prompt as key in YAML mode
        q_count += 1
    assert q_count > 0
    summary = agent.get_summary()
    assert isinstance(summary, dict)
    assert len(summary) == q_count

