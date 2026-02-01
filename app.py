import streamlit as st
from groq import Groq

# 1. MUDANÇA AQUI: Alterado para "expanded" para ela já começar aberta se preferir, 
# ou manter "auto" para o Streamlit decidir.
st.set_page_config(
    page_title="ChatFic AI", 
    layout="wide", 
    initial_sidebar_state="expanded" # Isso força ela a aparecer logo de cara
)

st.markdown("""
    <style>
    /* GARANTIR QUE O BOTÃO DAS 3 BARRINHAS APAREÇA */
    header[data-testid="stHeader"] {
        visibility: visible !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Cor do ícone das 3 barrinhas (preto para aparecer no fundo branco) */
    header button {
        color: #1a1a1a !important;
    }

    /* ESTILO DA SIDEBAR IGUAL À FOTO 11967 */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        min-width: 300px !important;
    }
    
    /* Estilizando os botões dentro da Sidebar para serem roxos e ovais */
    [data-testid="stSidebar"] .stButton button {
        background-color: #5D5FEF !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        margin-bottom: 10px !important;
    }

    /* Texto da Sidebar */
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #1a1a1a !important;
        font-family: 'Inter', sans-serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
