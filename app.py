import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "uid" not in st.session_state:
    st.session_state.uid = None
if "id_token" not in st.session_state:
    st.session_state.id_token = None
if "history" not in st.session_state:
    st.session_state.history = []

# Auth pages
if not st.session_state.logged_in:
    st.title("Emotional Wellness Chatbot")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            res = requests.post(f"{API_URL}/auth/login", json={
                "email": email, "password": password
            }).json()
            if "error" in res:
                st.error(res["error"])
            elif not res.get("email_verified"):
                st.warning("Please verify your email before logging in.")
            else:
                st.session_state.logged_in = True
                st.session_state.uid = res["uid"]
                st.session_state.id_token = res["id_token"]
                st.rerun()

    with tab2:
        name = st.text_input("Name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        age_group = st.selectbox("Age Group", ["13-17", "18-24", "25-34", "35-44", "45+"])
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
        if st.button("Register"):
            res = requests.post(f"{API_URL}/auth/register", json={
                "email": email,
                "password": password,
                "name": name,
                "age_group": age_group,
                "gender": gender
            }).json()
            if "error" in res:
                st.error(res["error"])
            else:
                st.success("Registered! Check your email to verify your account.")

# Chat page
else:
    st.title("How are you feeling today?")
    if st.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.session_state.uid = None
        st.session_state.history = []
        st.rerun()

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Talk to me...")
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        response = requests.post(f"{API_URL}/chat", json={
            "user_id": st.session_state.uid,
            "message": user_input,
            "chat_history": st.session_state.history
        }).json()

        reply = response["reply"]
        suggestion = response.get("suggestion")

        with st.chat_message("assistant"):
            st.write(reply)
            if suggestion:
                st.info("💙 " + "\n".join(suggestion))

        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": reply})