import streamlit as st
import json
import os
import sys

# Local imports
sys.path.append(os.path.abspath('.'))
from src.models.agent.concussion_agent import ConcussionAgent
from src.utils.protocols.concussion_flow import CONCUSSION_FLOW

st.set_page_config(page_title="Concussion Agent", page_icon="🧠")

st.title("🧠 Concussion Reporting Agent")
st.write("This assistant helps you collect key details after a possible concussion and prepares a structured summary for follow-up.")

# --- Session state ---
if "agent" not in st.session_state:
    st.session_state.agent = ConcussionAgent(CONCUSSION_FLOW)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "awaiting_input" not in st.session_state:
    st.session_state.awaiting_input = False
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# --- Ask the next question ---
def ask_next():
    next_q = st.session_state.agent.get_next_question()
    if next_q:
        st.session_state.current_question = next_q
        st.session_state.chat_history.append(("🤖", next_q))
        st.session_state.awaiting_input = True
    else:
        st.session_state.awaiting_input = False

# --- Show chat history ---
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(message)

# --- Capture user input ---
# --- Get user input ---
user_input = None
if st.session_state.awaiting_input:
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
        # Force early return to prevent multiple processing
        st.stop()

# --- Start button (only when idle) ---
if not st.session_state.awaiting_input and not st.session_state.agent.is_complete():
    if st.button("🟢 Start Reporting"):
        ask_next()

# --- Show final summary ---
if st.session_state.agent.is_complete():
    st.markdown("### ✅ Summary of Responses")
    st.json(st.session_state.agent.get_summary())

# --- Reset session ---
if st.button("🔁 Reset Session"):
    st.session_state.clear()
    st.rerun()
