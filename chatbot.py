import streamlit as st
from google import genai

# --- Config ---
API_KEY = "AIzaSyA2pMxpHoUETawkLPWWPqQGiZYev8ZJgQA"
KB_FILE = "irctc document.txt"
MODEL = "gemini-2.5-flash"

# --- Load KB ---
def load_kb():
    with open(KB_FILE, "r") as f:
        return f.read()

def create_chat():
    kb = load_kb()
    prompt = f"""
You are the IRCTC customer care executive. Your job is to answer the questions
asked by the customers and it should be in a polite way.
If any questions that are out of the kb you can tell them that I'm not aware of
this query. Please call customer help line number.
{kb}
"""
    client = genai.Client(api_key=API_KEY)
    chat = client.chats.create(
        model=MODEL,
        config={"system_instruction": prompt}
    )
    return client, chat  # keep client alive alongside chat

# --- Init session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    client, chat = create_chat()
    st.session_state.client = client  # store client to prevent it from closing
    st.session_state.chat = chat

# --- UI ---
st.title("IRCTC Customer Care")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if user_input := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = st.session_state.chat.send_message(user_input)
    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)