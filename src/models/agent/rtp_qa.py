
import json
from typing import Dict
from src.models.llm_openai import call_openai_chat
from src.utils.protocols.rtp_utils import find_current_stage, summarize_bundle, summarize_rtp_protocol, parse_llm_rtp_response

def generate_rtp_response_rule_based(activity_name: str, assessment_bundle: Dict, rtp_reference: list) -> Dict:
    matched_stage = None
    for stage in rtp_reference:
        if activity_name.lower() in [a.lower() for a in stage.get("allowed_activities", [])]:
            matched_stage = stage
            break

    if not matched_stage:
        return {
            "activity_match": False,
            "allowed": "uncertain",
            "stage_required": None,
            "reason": f"Activity '{activity_name}' not found in return-to-play protocol.",
            "recommendations": "We couldn’t locate that activity in the RTP protocol. Please rephrase or ask about a common activity.",
            "citations": []
        }

    current_stage = find_current_stage(assessment_bundle.get("responses", {}))
    required_stage_id = matched_stage["stage_id"]
    required_stage_name = matched_stage["name"]

    stage_index = {s["stage_id"]: i for i, s in enumerate(rtp_reference)}
    allowed = "uncertain"
    reason = ""
    if current_stage and current_stage in stage_index:
        if stage_index[current_stage] >= stage_index[required_stage_id]:
            allowed = "yes"
            reason = f"User is at {current_stage}, which meets or exceeds requirement for {required_stage_id}."
        else:
            allowed = "no"
            reason = f"User is currently in {current_stage}, but {activity_name} is not allowed until {required_stage_id}."

    system_prompt = """You are an assistant answering return-to-play questions about a player recovering from a concussion.

Use the player's current status and the concussion protocol to give activity-specific advice.

Return your response as plain markdown (no code fences). Be clear, supportive, and cite the protocol stage where possible.

Always include a gentle disclaimer: this is not a medical diagnosis."""

    user_payload = {
        "activity": activity_name,
        "current_stage": current_stage,
        "required_stage": required_stage_id,
        "assessment_responses": assessment_bundle.get("responses", {}),
        "symptoms": assessment_bundle.get("responses", {}).get("symptoms", {}),
        "stage_info": matched_stage
    }

    user_prompt = json.dumps(user_payload, indent=2)
    response_text = call_openai_chat(system_prompt=system_prompt, user_prompt=user_prompt)

    return {
        "activity_match": True,
        "allowed": allowed,
        "stage_required": required_stage_name,
        "reason": reason,
        "recommendations": response_text.strip(),
        "citations": matched_stage.get("citations", [])
    }

def generate_rtp_response_llm(user_question: str, assessment_bundle: dict, rtp_reference: list) -> dict:
    system_prompt = (
        "You are a return-to-play assistant helping a coach or parent interpret a player's recovery stage.\n"
        "You must only answer using the RTP protocol provided. DO NOT guess or invent.\n"
        "If unsure, say so and refer the user to a qualified healthcare professional.\n"
        "Return your answer in plain markdown.\n"
    )

    user_prompt = f"""
User asked: "{user_question}"

The player's current assessment bundle is:
{summarize_bundle(assessment_bundle)}

Here is the return-to-play protocol:
{summarize_rtp_protocol(rtp_reference)}

Based on the user's question, the recovery status, and the protocol, answer helpfully and clearly.
"""

    response_text = call_openai_chat(system_prompt=system_prompt, user_prompt=user_prompt)
    return parse_llm_rtp_response(response_text)
