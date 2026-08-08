import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Мій ШІ", page_icon="🤖")
st.title("🤖 Мій власний ШІ-асистент")

# Отримуємо API-ключ з налаштувань
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.warning("⚠️ Будь ласка, додайте GROQ_API_KEY в налаштуваннях Secrets у Streamlit Cloud!")
    st.stop()

client = Groq(api_key=api_key)

# Ініціалізація історії розмови
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Ти свій власний персональний ШІ-асистент. Відповідай дружньо та чітко."}
    ]

# Відображення збереженої історії
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Введення нового повідомлення
if prompt := st.chat_input("Спитай щось..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                response = completion.choices[0].message.content
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Помилка: {e}")
