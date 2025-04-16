import openai
import json
from src.models.llm_openai import call_openai_chat

def generate_llm_guidance(responses: dict, protocol: str = "ONF") -> str:
    # Flatten values
    flat = {
        k: (v["value"] if isinstance(v, dict) else v)
        for k, v in responses.items()
    }

    system_prompt = (
        f"You are a helpful assistant trained to provide return-to-play guidance "
        f"for youth sports concussions based on the {protocol} protocol. "
        f"Your advice should be clear, evidence-based, and prioritize player safety. "
        f"Include caveats that this is not medical advice. Always recommend seeing a qualified provider for diagnosis and clearance."
    )

    user_prompt = (
        f"Here is a summary of the concussion report in JSON:\n"
        f"{json.dumps(flat, indent=2)}\n\n"
        f"Please provide guidance based on this input."
    )

    response = call_openai_chat(system_prompt, user_prompt)
    return response.strip()
