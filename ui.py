import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="RoleBot 🤖",
    page_icon="🤖",
    layout="centered"
)

# --- HEADER ---
st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>RoleBot</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>💼 Your Role-Changing AI Agent</p>",
    unsafe_allow_html=True
)

# API URL
API_URL = "http://127.0.0.1:8000/chat"

# Model selection
MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x7b-32768"]

# --- INPUTS ---
with st.form("role_form"):
    given_system_prompt = st.text_area("🧠 Define the AI Agent's Role", height=80, placeholder="e.g., You are an expert Python tutor...")
    selected_model = st.selectbox("🧬 Choose a Model", MODEL_NAMES)
    user_input = st.text_area("🗨️ Message to AI", height=100, placeholder="Type your message...")
    submit = st.form_submit_button("🚀 Send Message")

# --- RESPONSE HANDLING ---
if submit:
    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "messages": [user_input],
                    "model_name": selected_model,
                    "system_prompt": given_system_prompt
                }
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    response_data = response.json()
                    ai_responses = [
                        msg.get("content", "")
                        for msg in response_data.get("messages", [])
                        if msg.get("type") == "ai"
                    ]
                    if ai_responses:
                        st.success("✅ AI Response:")
                        st.markdown(f"**{ai_responses[-1]}**")
                    else:
                        st.warning("No AI response found.")
                else:
                    st.error(f"Error {response.status_code}: Unable to fetch response.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
