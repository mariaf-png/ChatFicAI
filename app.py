import streamlit as st
from groq import Groq
import time

# 1. FORÇAR MODO CLARO E ÍCONE DE MENU (3 BARRINHAS)
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Faz as 3 barrinhas aparecerem no topo
)

# 2. CSS "BLINDADO" PARA VISIBILIDADE TOTAL
st.markdown("""
    <style>
    /* Fundo Branco Puro e Texto Preto para nada ficar invisível */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Esconder elementos desnecessários do Streamlit */
    header, footer { visibility: hidden !important; }

    /* Estilizando as Caixas de Texto (Inputs) para serem bem visíveis */
    .stTextInput input, .stTextArea textarea {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 2px solid #7d33ff !important;
        border-radius: 10px !important;
    }

    /* Título Roxo Grande */
    .main-title {
        color: #7d33ff !important;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-top: -40px;
    }

    /* Botão Roxo com Texto Branco */
    .stButton button {
        background-color: #7d33ff !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* Garantir que o texto do menu lateral apareça */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #7d33ff;
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE NAVEGAÇÃO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# 4. BARRA LATERAL (CLIQUE NAS 3 BARRINHAS NO TOPO ESQUERDO)
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    st.button("👤 Login / Cadastro")
    st.divider()
    if st.button("➕ Nova Fanfic"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 5. PÁGINA INICIAL
if st.session_state.page == "home":
    st.markdown("<h1 class='main-title'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #555;'>Crie histórias incríveis com IA</p>", unsafe_allow_html=True)
    
    # Campos de preenchimento
    fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Marvel, Naruto...")
    titulo = st.text_input("Título da História", placeholder="Ex: O Retorno do Herói")
    
    # Caixa de diálogo para o prompt como você pediu
    instrucao = st.text_area("Como você quer a sua história?", 
                            placeholder="Ex: Quero que a história comece em uma noite chuvosa e tenha muito mistério...")
    
    if st.button("GERAR HISTÓRIA ✨"):
        if fandom and titulo and instrucao:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.instrucao = instrucao
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos acima!")

# 6. PÁGINA DE CHAT
else:
    st.markdown(f"<h2 style='text-align:center; color:#7d33ff;'>{st.session_state.titulo}</h2>", unsafe_allow_html=True)
    
    # Exibir histórico de mensagens
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Gerar a primeira resposta automaticamente
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt_full = f"Escreva o capítulo 1 de uma fanfic do universo {st.session_state.fandom}. Detalhes: {st.session_state.instrucao}. Título: {st.session_state.titulo}."
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Você é um escritor de fanfics profissional."},
                              {"role": "user", "content": prompt_full}]
                )
                
                txt = res.choices[0].message.content
                st.write(txt)
                st.session_state.messages.append({"role": "assistant", "content": txt})
            except:
                st.error("Erro: Verifique sua chave API do Groq no painel do Streamlit!")

    # Entrada para continuar a história
    if prompt := st.chat_input("O que acontece depois?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
