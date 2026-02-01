import streamlit as st
from groq import Groq
import time

# 1. FORÇAR TEMA CLARO E MENU
st.set_page_config(
    page_title="ChatFic AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS PARA CLONAR O NETLIFY (Fundo Branco + Roxo)
st.markdown("""
    <style>
    /* Reset de Fundo e Texto - Para nada ficar invisível */
    .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }

    /* BARRA LATERAL IDENTICA AO APP (Roxa) */
    [data-testid="stSidebar"] {
        background-color: #7d33ff !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] { background-image: none !important; }

    /* Esconder cabeçalhos nativos feios */
    header, footer { visibility: hidden !important; }

    /* Ajuste das Caixas de Texto (Inputs) - Sem o "preto" estranho */
    .stTextInput input, .stTextArea textarea {
        background-color: #f8f9fa !important;
        color: #1a1a1a !important;
        border: 2px solid #e9ecef !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #7d33ff !important;
        box-shadow: 0 0 0 1px #7d33ff !important;
    }

    /* Labels (Títulos das caixas) sempre pretos */
    label p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }

    /* BOTÃO ROXO ARREDONDADO (IGUAL AO NETLIFY) */
    .stButton button {
        background-color: #7d33ff !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 12px 25px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        transition: 0.3s !important;
    }
    .stButton button:hover {
        background-color: #6221d8 !important;
        transform: translateY(-2px);
    }

    /* Título ChatFic AI */
    .main-title {
        color: #7d33ff !important;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-top: -50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE NAVEGAÇÃO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (CLIQUE NAS 3 BARRINHAS NO TOPO)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>ChatFic AI</h2>", unsafe_allow_html=True)
    st.divider()
    st.button("👤 Perfil / Login")
    st.button("⚙️ Configurações")
    if st.button("➕ Nova História"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 4. PÁGINA INICIAL
if st.session_state.page == "home":
    st.markdown("<p style='text-align:center; font-size: 60px;'>📖</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6c757d;'>Crie histórias incríveis com IA</p>", unsafe_allow_html=True)
    
    fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Marvel, Harry Potter")
    titulo = st.text_input("Título da História", placeholder="Ex: O Retorno do Herói")
    instrucao = st.text_area("Como você quer
    
