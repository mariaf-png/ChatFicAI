import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DE PÁGINA
st.set_page_config(
    page_title="ChatFic AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS PARA CORRIGIR TUDO (VISIBILIDADE E 3 BARRINHAS)
st.markdown("""
    <style>
    /* Forçar Fundo Branco e Texto Preto em TUDO */
    .stApp, div[data-testid="stSidebarContent"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Forçar Labels (Etiquetas) a serem Pretas e Visíveis */
    label, p, span, .stMarkdown {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    /* Ajustar Caixas de Entrada para fundo cinza claro (estilo iPhone/Moderno) */
    .stTextInput input, .stTextArea textarea, [data-baseweb="select"] {
        background-color: #f2f2f7 !important;
        color: #000000 !important;
        border: 1px solid #d1d1d6 !important;
    }

    /* Botão Principal Roxo */
    .stButton button {
        background-color: #7d33ff !important;
        color: #ffffff !important;
        border-radius: 25px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
    }

    /* MOSTRAR AS 3 BARRINHAS (Menu nativo do Streamlit) */
    header {
        visibility: visible !important;
        background-color: #ffffff !important;
    }
    
    /* Centralizar Título */
    .main-title {
        color: #7d33ff !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE NAVEGAÇÃO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (MENU DAS 3 BARRINHAS)
with st.sidebar:
    st.markdown("<h2 style='color:#7d33ff;'>Menu</h2>", unsafe_allow_html=True)
    st.button("👤 Perfil / Login")
    st.divider()
    if st.button("➕ Criar Nova História"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 4. PÁGINA INICIAL
if st.session_state.page == "home":
    st.markdown("<p style='text-align:center; font-size: 50px;'>📖</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Crie histórias incríveis com IA</p>", unsafe_allow_html=True)
    
    # Inputs com labels agora pretas e visíveis
    fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Harry Potter")
    titulo = st.text_input("Título da História", placeholder="Ex: A Nova Jornada")
    instrucao = st.text_area("Como você quer a sua história?", 
                            placeholder="Descreva aqui o enredo inicial...")
    
    if st.button("GERAR HISTÓRIA ✨"):
        if fandom and titulo and instrucao:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.instrucao = instrucao
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Preencha todos os campos!")

# 5. PÁGINA DE CHAT
else:
    st.markdown(f"<h2 style='text-align:center; color:#7d33ff;'>{st.session_state.titulo}</h2>", unsafe_allow_html=True)
    
    # Histórico
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # IA (Groq)
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt_ia = f"Escreva o capítulo 1 da fanfic {st.session_state.titulo} no universo {st.session_state.fandom}. Instrução: {st.session_state.instrucao}."
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_ia}]
                )
                txt = res.choices[0].message.content
                st.write(txt)
                st.session_state.messages.append({"role": "assistant", "content": txt})
            except:
                st.error("Erro na API! Verifique os Secrets do Streamlit.")

    if prompt := st.chat_input("Continue a história..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
