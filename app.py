# app.py
import streamlit as st
import requests
import json
from datetime import datetime

# ========== CONFIGURATION ==========
# 💡 Replace with your actual Groq API key and model
GROQ_API_KEY = "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"  # <<<--- put your key here
MODEL_NAME = "llama-3.1-70b-versatile"          # example model; change if needed
API_URL = f"https://api.groq.com/openai/v1/chat/completions"

# ========== STREAMLIT UI SETUP ==========
st.set_page_config(page_title="Zain Ul Islam Adil ChatBot", layout="centered")
st.title("Zain Ul Islam Adil ChatBot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
    max_tokens = st.number_input("Max Tokens", 100, 2000, 512, 50)
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        st.experimental_rerun()

# ========== CHAT DISPLAY ==========
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **Bot:** {msg['content']}")

# ========== USER INPUT ==========
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"🧑 **You:** {user_input}")

    # Prepare request payload
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # ========== API CALL ==========
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            # Extract response text
            bot_message = result["choices"][0]["message"]["content"].strip()

            # Append to conversation
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
            st.markdown(f"🤖 **Bot:** {bot_message}")

        except Exception as e:
            st.error(f"❌ Error: {e}")
