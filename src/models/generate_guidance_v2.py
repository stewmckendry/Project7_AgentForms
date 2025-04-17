
import json
from typing import Dict
from src.models.llm_openai import call_openai_chat

def generate_guidance(assessment_bundle: Dict) -> Dict:
    responses = assessment_bundle.get("responses", {})
    followups = assessment_bundle.get("followup_log", [])
    symptom_reference = assessment_bundle.get("symptom_reference", {})
    rtp_reference = assessment_bundle.get("return_to_play_reference", {})

    system_prompt = """You are an AI assistant helping a parent or coach understand whether a player is ready to return to play after a possible concussion.

You will receive:
- Structured answers to medical questions
- Reasoning ("thoughts") for each answer
- Follow-up dialogue with the user
- A reference of concussion symptoms and severity
- A staged return-to-play protocol with descriptions, progression rules, and risks

Your job:
1. Identify whether the symptoms and activity suggest a suspected concussion
2. Determine the most appropriate return-to-play stage
3. Provide clear, personalized guidance on what the user should and should not do
4. Flag any risks, red flags, or uncertainty in the responses
5. Explain the "why" behind each recommendation
6. Encourage the user and remind them that this is not a medical diagnosis

Return your output as a JSON object with the following fields:
- summary: One-line summary
- stage_recommendation: Stage ID from the protocol
- full_guidance: Markdown-safe explanation (no code fences)

Tone: compassionate, conversational, and helpful. Target: concerned parent or coach."""

    user_prompt_payload = {
        "assessment_responses": responses,
        "followup_log": followups,
        "symptom_reference": symptom_reference,
        "return_to_play_protocol": rtp_reference
    }

    user_prompt = json.dumps(user_prompt_payload, indent=2)

    # Call wrapped OpenAI interface
    raw_output = call_openai_chat(system_prompt=system_prompt, user_prompt=user_prompt)

    try:
        parsed_output = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed_output = {
            "summary": "We could not parse the AI response.",
            "stage_recommendation": "unknown",
            "full_guidance": raw_output.strip()
        }

    return parsed_output
