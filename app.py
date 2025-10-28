import streamlit as st
import requests
import json

# ===========================
# CONFIGURATION
# ===========================
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")

# 🔑 Embed your Groq API key here
API_KEY = "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"  # ← Replace with your actual API key

# Default model (you can change it)
MODEL_NAME = "llama3-70b-8192"

# ===========================
# UI HEADER
# ===========================
st.title("🤖 Groq Chatbot")
st.caption("Chatbot powered by Groq large language models — built by Zain Ul Islam Adil")

# ===========================
# Initialize Chat Memory
# ===========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===========================
# User Input
# ===========================
prompt = st.chat_input("Type your message here...")

if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Prepare request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": st.session_state.messages,
            "temperature": 0.7
        }

        # Send request
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        # Handle response
        if response.status_code != 200:
            st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
        else:
            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            st.chat_message("assistant").markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
