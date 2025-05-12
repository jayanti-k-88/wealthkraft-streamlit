import streamlit as st
import requests

API_URL = "http://13.234.57.143:7860/api/v1/run/2e4d4511-ba44-4bd2-ae2a-6c25671f6e61"

def send_message_to_backend(user_message):
    payload = {
        "input_type": "chat",
        "output_type": "chat",
        "input_value": user_message
    }
    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()
        return data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except Exception as e:
        return f"[Error] {e}"

def handle_chat():
    st.markdown("##### 💬 Chat with Finnie")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hey Finnie, help me with my finances."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        response = send_message_to_backend(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
