from src.utils.logging.logger import setup_logger
logger = setup_logger()

def generate_guidance(responses):
    logger.info("Concussion guidance generation started - the only static rules version")
    
    if not responses:
        return "No data available to provide guidance."

    messages = []

    if get_value(responses, "What symptoms did the player experience after the incident?"):
        messages.append("⚠️ Symptoms were reported — the player should be evaluated by a healthcare provider.")

    if not get_value(responses, "Has the player been seen by a healthcare provider?"):
        messages.append("📋 Encourage a medical evaluation to confirm if a concussion occurred.")

    if get_value(responses, "Is the player still experiencing symptoms?") is True:
        messages.append("🚫 Player is not ready for return to play. They must be symptom-free before progressing.")

    if get_value(responses,"Has the player been cleared to return to play by a professional?") is not True:
        messages.append("🩺 Clearance is required from a medical professional before resuming sport.")

    if not messages:
        messages.append("✅ The player appears to meet conditions for return to play. Please proceed carefully through stages.")

    return "\n\n".join(messages)


def get_value(responses, key):
    val = responses.get(key)
    if isinstance(val, dict) and "value" in val:
        return val["value"]
    return val