
from typing import Dict, List

def find_current_stage(responses: Dict) -> str:
    '''
    Very basic rule-based logic to infer current RTP stage.
    Could be replaced later by LLM.
    '''
    if not responses:
        return "unknown"

    if responses.get("still_symptomatic", {}).get("value") == "yes":
        return "stage_1"

    if responses.get("cleared_to_play", {}).get("value") == "yes":
        return "stage_6"

    return "stage_2"  # placeholder fallback

def summarize_bundle(assessment_bundle: Dict) -> str:
    '''
    Create a concise summary of key structured responses for LLM prompt context.
    '''
    responses = assessment_bundle.get("responses", {})
    summary = []
    for qid, entry in responses.items():
        val = entry.get("value")
        certainty = entry.get("certainty")
        summary.append(f"{qid}: {val} (certainty: {certainty})")
    return "\n".join(summary)

def summarize_rtp_protocol(rtp_reference: List[Dict]) -> str:
    '''
    Formats a short readable version of the RTP protocol for inclusion in an LLM prompt.
    '''
    lines = []
    for stage in rtp_reference:
        stage_id = stage.get("stage_id")
        name = stage.get("name")
        desc = stage.get("description")
        activities = ", ".join(stage.get("allowed_activities", []))
        lines.append(f"{stage_id} - {name}: {desc}")
        lines.append(f"Allowed: {activities}")
        lines.append("")
    return "\n".join(lines)

def parse_llm_rtp_response(response_text: str) -> Dict:
    '''
    Parses the LLM markdown response into structured fields.
    Can be upgraded later with regex or JSON parsing.
    '''
    return {
        "activity_match": True,
        "allowed": "uncertain",
        "stage_required": "unknown",
        "reason": "Parsed from LLM response.",
        "recommendations": response_text.strip(),
        "citations": []
    }
