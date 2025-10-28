import streamlit as st
import requests
import json

# ===========================
# CONFIGURATION
# ===========================
st.set_page_config(page_title="Zain Ul Islam Adil Chatbot", page_icon="🤖", layout="centered")

# Embed your Groq API key here
API_KEY = "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"  # ← Replace with your actual key

# A supported Groq model
MODEL_NAME = "llama-3.1-8b-instant"

# ===========================
# UI HEADER
# ===========================
st.title("Zain Ul Islam Adil")
st.caption("Chatbot powered by Groq developed by Zain Ul Islam Adil")

# ===========================
# Initialize Chat Memory
# ===========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display conversation
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(f"🧑 **You:** {content}")
    elif role == "assistant":
        st.markdown(f"🤖 **Bot:** {content}")
    else:
        st.markdown(f"**System:** {content}")

# ===========================
# User Input
# ===========================
user_input = st.text_input("Type your message here:", key="user_input")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare API request
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages,
        "temperature": 0.5,
        "max_tokens": 512
    }

    # Call the API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            # Extract assistant response (assuming common OpenAI-style structure)
            bot_reply = data["choices"][0]["message"]["content"]
            # Append to conversation
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            # Display bot reply
            st.markdown(f"🤖 **Bot:** {bot_reply}")

        except requests.exceptions.HTTPError as http_err:
            st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
        except Exception as err:
            st.error(f"⚠️ Error: {err}")
