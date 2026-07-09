import streamlit as st
import requests

st.title("Emotional Wellness Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "user_1"

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("How are you feeling today?")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    response = requests.post("http://127.0.0.1:8000/chat", json={
        "user_id": st.session_state.user_id,
        "message": user_input,
        "chat_history": st.session_state.history
    })

    data = response.json()
    reply = data["reply"]
    suggestion = data.get("suggestion")

    with st.chat_message("assistant"):
        st.write(reply)
        if suggestion:
            st.info("💙 " + "\n".join(suggestion))

    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": reply})