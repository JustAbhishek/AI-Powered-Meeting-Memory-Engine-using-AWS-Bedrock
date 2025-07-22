import streamlit as st
import requests
import json
import os

# App Config
st.set_page_config(page_title="Meeting Insights", layout="centered")

# --- Styles ---
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #1f4e79;
            font-size: 2.2rem;
        }
        .stTextInput > label, .stTextArea > label {
            font-weight: 600 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📋 Meeting Intelligence</h1>", unsafe_allow_html=True)
st.markdown("Ask insights from meeting recordings with context-aware responses.")

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "company" not in st.session_state:
    st.session_state.company = ""

# --- Real API Call ---
def call_api(question, company=None):
    url = "https://ym8w92784e.execute-api.us-east-1.amazonaws.com/Prod/query"  # 🔁 Replace with your actual endpoint
    payload = {
        "question": question,
    }
    if company:
        payload["company"] = company

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# --- Render Answer Nicely ---
def render_answer(answer):
    lines = answer.strip().split("\n")
    for line in lines:
        clean = line.strip().lstrip('-•1234567890. ').strip()
        if clean:
            st.markdown(f"- {clean}")

# --- Main Question Form ---
with st.form("main_question_form"):
    question = st.text_input("🔍 Your Question", placeholder="e.g., What decisions were made by Transrail?")
    company = st.text_input("🏢 Company (Optional)", placeholder="e.g., TRANSRAIL")
    main_submit = st.form_submit_button("💡 Get Insight")

if main_submit and question:
    with st.spinner("Thinking..."):
        payload_question = question
        payload_company = company.upper() if company else None

        st.session_state.company = payload_company or ""
        data = call_api(payload_question, payload_company)
        if data:
            answer = data.get("llm_response", {}).get("answer")
            if answer:
                st.session_state.last_question = payload_question
                st.session_state.last_answer = answer
                st.session_state.history.append((payload_question, answer))

                st.markdown("### ✅ Answer")
                render_answer(answer)
            else:
                st.warning("No answer found in response.")
        else:
            st.error("No response received from API.")

# --- Follow-up Form ---
if st.session_state.last_answer:
    with st.form("follow_up_form"):
        st.markdown("### 🔄 Follow-up Question")
        follow_up = st.text_input("Ask something more...", key="follow_up_input")
        follow_submit = st.form_submit_button("➡️ Submit Follow-up")

    if follow_submit and follow_up:
        with st.spinner("Thinking..."):
            context = f"Previous Q: {st.session_state.last_question}\nPrevious A: {st.session_state.last_answer}\nFollow-up: {follow_up}"
            payload_company = st.session_state.company

            data = call_api(context, payload_company)
            if data:
                answer = data.get("llm_response", {}).get("answer")
                if answer:
                    st.session_state.last_question = follow_up
                    st.session_state.last_answer = answer
                    st.session_state.history.append((follow_up, answer))

                    st.markdown("### ✅ Answer")
                    render_answer(answer)
                else:
                    st.warning("No answer found in response.")
            else:
                st.error("No response received from API.")

# --- History Viewer ---
with st.expander("🕘 View Previous Questions"):
    for i, (q, a) in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**Q{i}:** {q}")
        st.markdown(f"**A{i}:** {a}")
        st.markdown("---")

# --- Export as JSON ---
if st.session_state.history:
    if st.button("📥 Download Q&A History as JSON"):
        export_path = os.path.join("exports", "chat_history.json")
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        export_data = [{"question": q, "answer": a} for q, a in st.session_state.history]
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2)
        st.success(f"Chat history exported to `{export_path}`")
