import streamlit as st
import requests
import json

# ===========================
# Streamlit App Configuration
# ===========================
st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Groq Chatbot")
st.caption("Chatbot powered by Groq large language models — built by Zain Ul Islam Adil")

# ===========================
# Sidebar for API Key & Model
# ===========================
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("🔑 Enter your Groq API Key", type="password")

model_name = st.sidebar.selectbox(
    "🧠 Choose Model",
    [
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it"
    ],
    index=0
)

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
# Chat Input Box
# ===========================
prompt = st.chat_input("Type your message here...")

if prompt:
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()

    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Prepare API call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_name,
            "messages": st.session_state.messages,
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        # Handle Response
        if response.status_code != 200:
            st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
        else:
            result = response.json()
            bot_reply = result["choices"][0]["message"]["content"]
            st.chat_message("assistant").markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
