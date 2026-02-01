import streamlit as st
from groq import Groq
import time

# 1. SETUP: FORÇA O MENU E O TEMA
st.set_page_config(
    page_title="ChatFic AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS "CLONE" (Fundo Branco, Botão Roxo Oval e Sidebar Roxa)
st.markdown("""
    <style>
    /* Forçar fundo branco total no corpo do site */
    .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }

    /* BARRA LATERAL (SIDEBAR) - Roxo Sólido igual ao Netlify */
    [data-testid="stSidebarContent"] {
        background-color: #7d33ff !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebarContent"] * {
        color: #ffffff !important;
    }

    /* Esconder o cabeçalho preto do Streamlit que está atrapalhando */
    header { background-color: rgba(0,0,0,0) !important; }
    footer { visibility: hidden !important; }

    /* INPUTS: Estilo limpo, sem fundo preto ou cinza escuro */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border: 2px solid #7d33ff !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }

    /* BOTÃO: Roxo, Texto Branco e OVAL (Pill shape) */
    .stButton button {
        background-color: #7d33ff !important;
        color: #ffffff !important;
        border-radius: 50px !important; /* Deixa o botão oval */
        border: none !important;
        font-weight: bold !important;
        padding: 0.6rem 2rem !important;
        width: 100% !important;
    }
    .stButton button:hover {
        background-color: #6221d8 !important;
        color: #ffffff !important;
    }

    /* TÍTULO: Roxo e Centralizado */
    .main-title {
        color: #7d33ff !important;
        text-align: center;
        font-size: 3.2rem;
        font-weight: 900;
        margin-top: -60px;
    }

    /* Labels das caixas (o texto em cima delas) */
    label p {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. NAVEGAÇÃO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (Acessível pelo ícone de 3 barrinhas no topo)
with st.sidebar:
    st.markdown("### ⚙️ Opções")
    st.button("👤 Perfil / Login")
    st.divider()
    if st.button("➕ Nova História"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 4. PÁGINA INICIAL (Layout idêntico ao Netlify)
if st.session_state.page == "home":
    st.markdown("<p style='text-align:center; font-size: 80px; margin-bottom: 0;'>📖</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#555; margin-bottom: 30px;'>Crie histórias incríveis com IA</p>", unsafe_allow_html=True)
    
    # Organizando os campos
    fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Marvel, Harry Potter")
    titulo = st.text_input("Título da História", placeholder="Ex: O Retorno do Herói")
    instrucao = st.text_area("Como você quer a sua história?", placeholder="Ex: Comece com um mistério...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GERAR HISTÓRIA ✨"):
        if fandom and titulo and instrucao:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.instrucao = instrucao
            st.session_state.page = "chat"
            st.rerun()

# 5. PÁGINA DE CHAT
else:
    st.markdown(f"<h2 style='text-align:center; color:#7d33ff;'>{st.session_state.titulo}</h2>", unsafe_allow_html=True)
    
    # Chat History
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Primeira resposta automática (Memória do Prompt Inicial)
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt_ia = f"Inicie o capítulo 1 da fanfic {st.session_state.titulo} no universo {st.session_state.fandom}. Instrução: {st.session_state.instrucao}."
                
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_ia}]
                )
                txt = res.choices[0].message.content
                st.write(txt)
                st.session_state.messages.append({"role": "assistant", "content": txt})
            except:
                st.error("Erro na API. Verifique os Secrets do Streamlit.")

    if prompt := st.chat_input("Diga o que acontece agora..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
        
