import streamlit as st
import json
import os
import sys

# Local imports
sys.path.append(os.path.abspath('.'))
from src.models.agent.concussion_agent import ConcussionAgent
from src.utils.protocols.load_concussion_flow import load_concussion_flow
from src.models.llm_guidance import generate_llm_guidance
from src.utils.output.exporter import export_json, export_markdown
from src.utils.logging.logger import setup_logger
logger = setup_logger()
logger.info("Streamlit app started")

st.set_page_config(page_title="Concussion Agent", page_icon="🧠")

st.title("🧠 Concussion Reporting Agent")
st.write("This assistant helps you collect key details after a possible concussion and prepares a structured summary for follow-up.")

# --- Session state ---
if "agent" not in st.session_state:
    CONCUSSION_FLOW = load_concussion_flow()
    st.session_state.agent = ConcussionAgent(CONCUSSION_FLOW)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_input" not in st.session_state:
    st.session_state.awaiting_input = False
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "flow_started" not in st.session_state:
    st.session_state.flow_started = False
if "known_questions" not in st.session_state:
    st.session_state.known_questions = []

# --- Sidebar ---
with st.expander("🔍 Debug Session State"):
    st.write("flow_started:", st.session_state.get("flow_started"))
    st.write("awaiting_input:", st.session_state.get("awaiting_input"))
    st.write("current_question:", st.session_state.get("current_question"))
    st.write("agent complete:", st.session_state.agent.is_complete())
    st.write("chat history length:", len(st.session_state.chat_history))

"""
# --- Step 1: Gather the incident details ---#
st.markdown("### 📝 Tell us what happened")

user_story = st.text_area("Describe the incident in your own words:")

if st.button("Start Assessment"):
    st.session_state.agent.record_freeform_analysis(user_story, st.session_state.agent.known_questions)
    st.success("Initial analysis complete. You can now continue the conversation.")
"""

# --- Ask the next question ---
def ask_next():
    next_q = st.session_state.agent.get_next_question()
    if next_q:
        st.session_state.current_question = next_q
        st.session_state.chat_history.append(("🤖", next_q))
        st.session_state.awaiting_input = True
    else:
        st.session_state.awaiting_input = False

# --- Start button (only when idle) ---
if not st.session_state.awaiting_input and not st.session_state.agent.is_complete():
    if not st.session_state.flow_started:
        if st.button("🟢 Start Reporting"):
            st.session_state.flow_started = True
            ask_next()
            # Update screen with first question
            st.rerun()

# --- Show chat history ---
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

# --- Capture user input ---
# --- Get user input ---
user_input = None
if st.session_state.flow_started and st.session_state.awaiting_input and st.session_state.current_question:
    user_input = st.chat_input("Your answer:")
    if user_input:
        # Process it immediately
        st.session_state.chat_history.append(("👤", user_input))
        q = st.session_state.current_question
        st.session_state.agent.record_response(q, user_input)
        # Clear state before rerun
        st.session_state.awaiting_input = False
        st.session_state.current_question = None
        # Ask the next question during same rerun
        with st.spinner("Thinking..."):
            ask_next()
        # Update screen with new question
        st.rerun()

# --- Show final summary ---
if st.session_state.agent.is_complete():
    st.markdown("### ✅ Summary of Responses")
    responses = st.session_state.agent.get_summary()
    st.json(responses)

    st.markdown("### 🤖 LLM-Powered Return-to-Play Guidance")
    llm_guidance = generate_llm_guidance(responses)
    st.markdown(llm_guidance)

    # --- Export buttons ---
    json_path = export_json(responses)
    md_path = export_markdown(st.session_state.chat_history, llm_guidance)

    with open(json_path, "rb") as f:
        st.download_button(
            label="⬇️ Download JSON Report",
            data=f,
            file_name=os.path.basename(json_path),
            mime="application/json"
        )

    with open(md_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Markdown Summary",
            data=f,
            file_name=os.path.basename(md_path),
            mime="text/markdown"
        )


# --- Reset session ---
if st.button("🔁 Reset Session"):
    st.session_state.clear()
    st.rerun()
