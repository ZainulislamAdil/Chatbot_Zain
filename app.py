import streamlit as st
import requests

# ========== CONFIG ==========
GROQ_API_KEY = "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"  # 🔑 Paste your Groq API key here
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-70b-versatile"  # ✅ Change if needed (Groq supports several)

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🤖 Groq Chatbot (Streamlit)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5)
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        st.experimental_rerun()

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"🤖 **Bot:** {msg['content']}")

# User input area
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"🧑 **You:** {user_input}")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages,
        "temperature": temperature,
        "max_tokens": 512
    }

    # Call Groq API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()

            bot_message = data["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
            st.markdown(f"🤖 **Bot:** {bot_message}")

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTP Error {e.response.status_code}: {e.response.text}")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
