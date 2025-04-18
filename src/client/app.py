# src/client/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8001"

st.set_page_config(page_title="Concussion Assistant", layout="centered")
st.title("🏒 Concussion Assistant")

if "mode" not in st.session_state:
    st.session_state.mode = None
if "assessment_bundle" not in st.session_state:
    st.session_state.assessment_bundle = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

mode = st.radio("How can I help today?", ["Assess a possible concussion", "Ask about return to play"])
st.session_state.mode = mode

if mode == "Assess a possible concussion":
    st.subheader("🧠 Step 1: Describe what happened")
    user_input = st.text_area("Describe the incident in your own words")
    if st.button("Analyze situation"):
        with st.spinner("Analyzing..."):
            res = requests.post(f"{API_URL}/analyze", json={"free_text": user_input})
            data = res.json()
            st.session_state.assessment_bundle = {"responses": data["draft_responses"], "summary_thought": data["summary_thought"]}
            st.success("Draft responses generated")
            st.write(data["summary_thought"])
            st.json(data["draft_responses"])

    if st.session_state.assessment_bundle:
        st.subheader("💬 Step 2: Generate Follow-Up Questions")
        followup_res = requests.post(f"{API_URL}/followups", json={
            "final_responses": st.session_state.assessment_bundle["responses"],
            "question_list": [{"id": k, "prompt": k, "type": v.get("type", "text")} for k, v in st.session_state.assessment_bundle["responses"].items()]
        })
        followups = followup_res.json().get("followups", [])
        for i, q in enumerate(followups):
            answer = st.text_input(f"{q}", key=f"followup_{i}")

        st.subheader("📋 Step 3: Get Return-to-Play Guidance")
        if st.button("Generate guidance"):
            guidance_res = requests.post(f"{API_URL}/guidance", json={"assessment_bundle": st.session_state.assessment_bundle})
            guidance_data = guidance_res.json()
            st.markdown(guidance_data["summary"])
            st.markdown(guidance_data["full_guidance"])

elif mode == "Ask about return to play":
    st.subheader("💬 Ask about an activity")
    user_question = st.chat_input("Ask a return-to-play question")
    if user_question:
        st.chat_message("user").write(user_question)
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        response = requests.post(f"{API_URL}/rtp/ask", json={
            "question": user_question,
            "assessment_bundle": st.session_state.assessment_bundle
        })
        reply = response.json()
        message = f"**Allowed?** {reply['allowed']}\n\n**Stage Required:** {reply['stage_required']}\n\n**Reason:** {reply['reason']}\n\n**Recommendations:**\n- " + "\n- ".join(reply.get("recommendations", []))
        st.chat_message("assistant").markdown(message)
        st.session_state.chat_history.append({"role": "assistant", "content": message})