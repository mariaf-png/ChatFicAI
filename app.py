import streamlit as st
from groq import Groq

# Configuração visual
st.set_page_config(page_title="ChatficIA", page_icon="✍️")
st.title("✍️ ChatficIA")

# Pegar a chave secreta
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configure a chave GROQ_API_KEY nos Secrets!")
    st.stop()

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Escreva sua fanfic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrução para a IA agir como ChatficIA
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é o ChatficIA, especialista em fanfics criativas em português."},
                {"role": "user", "content": prompt}
            ]
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
      
