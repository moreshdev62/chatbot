import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("MoreshAI")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Ты дружелюбный помощник по имени MoreshAI. Отвечай на русском."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Напиши сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
