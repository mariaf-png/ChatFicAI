import streamlit as st
from groq import Groq

# 1. FORÇAR ESTADO EXPANDIDO PARA EVITAR TELA VAZIA
st.set_page_config(
    page_title="ChatFic AI",
    layout="centered",
    initial_sidebar_state="expanded" 
)

# 2. CSS "LIMPO" PARA EVITAR TELA BRANCA E MANTER O DESIGN
st.markdown("""
    <style>
    /* Base da App - Fundo Branco */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* BARRA LATERAL (SIDEBAR) - IGUAL À FOTO 11967 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #F0F0F5 !important;
    }
    
    /* Botão Roxo Oval na Sidebar */
    [data-testid="stSidebar"] .stButton button {
        background-color: #5D5FEF !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 20px !important;
    }

    /* INPUTS ARREDONDADOS - IGUAL À FOTO 11965 */
    .stTextInput input, .stTextArea textarea {
        background-color: #F8F9FB !important;
        border: 1px solid #E6E8EB !important;
        border-radius: 20px !important;
        color: #1A1C1E !important;
    }

    /* BOTÃO GERAR - ROXO E OVAL */
    div.stButton > button:first-child {
        background-color: #5D5FEF !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100% !important;
        font-weight: bold !important;
    }

    /* Títulos em Preto para visibilidade total */
    h1, h2, h3, p, label {
        color: #1A1C1E !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Garante que o Header (Menu) não suma */
    header {
        visibility: visible !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INICIALIZAÇÃO DE VARIÁVEIS (ESSENCIAL PARA NÃO DAR TELA BRANCA)
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. MENU LATERAL
with st.sidebar:
    st.markdown("### 📖 ChatFic")
    if st.button("＋ Nova Fanfic"):
        st.session_state.page = "home"
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("🌍 Comunidade")
    st.markdown("⚙️ Configurações")

# 5. CONTEÚDO PRINCIPAL
if st.session_state.page == "home":
    st.markdown("<p style='text-align:center; font-size: 60px;'>📖</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Nova Fanfic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color: #6E7175;'>Sua próxima obra-prima começa agora.</p>", unsafe_allow_html=True)
    
    # Campos
    st.text_input("TÍTULO DA SUA OBRA...", placeholder="Dê um nome épico...")
    st.text_input("UNIVERSO (EX: MARVEL, ONE PIECE)", placeholder="Hogwarts, Gotham...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GERAR HISTÓRIA ✨"):
        st.session_state.page = "chat"
        st.rerun()

else:
    # Tela de Chat (simulada para evitar erro se não houver Groq configurado)
    st.markdown("<h2 style='text-align:center;'>Escrevendo...</h2>", unsafe_allow_html=True)
    if st.button("← Voltar"):
        st.session_state.page = "home"
        st.rerun()
