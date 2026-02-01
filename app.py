import streamlit as st
from groq import Groq
import time

# 1. FORÇAR MODO CLARO E MENU DE 3 BARRINHAS
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. CSS PARA DESIGN IDENTICO (MODO CLARO + ROXO VIBRANTE)
st.markdown("""
    <style>
    /* Fundo Branco e Texto Visível */
    .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Esconder cabeçalhos nativos feios */
    header, footer { visibility: hidden !important; }

    /* Inputs (Caixas de texto) escuras com texto branco como na sua foto */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #2d2d35 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 15px !important;
    }

    /* Título Roxo */
    .main-title {
        color: #7d33ff;
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        margin-top: -50px;
    }

    /* Botão Principal */
    .stButton button {
        background-color: #1a1a1a !important;
        color: #7d33ff !important;
        border: 2px solid #7d33ff !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        height: 50px !important;
        width: 100% !important;
    }

    /* Ajuste da Barra Lateral (3 Barrinhas) */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #7d33ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGICA DE ESTADO
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# 4. BARRA LATERAL (ACESSÍVEL PELAS 3 BARRINHAS NO TOPO ESQUERDO)
with st.sidebar:
    st.title("📖 ChatFic AI")
    st.divider()
    st.button("👤 Login / Cadastro")
    st.slider("Tamanho da Fonte", 14, 24, 18)
    if st.button("➕ Nova Fanfic"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 5. PÁGINA INICIAL
if st.session_state.page == "home":
    st.markdown("<div style='text-align:center;'><br>📖</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>ChatFic AI</h1>", unsafe_allow_html=True)
    
    # Inputs Identicos à sua imagem
    fandom = st.text_input("Universo/Fandom", placeholder="Ex: Harry Potter")
    titulo = st.text_input("Título da História", placeholder="Ex: A Pedra Filosofal 2")
    
    prompt_user = st.text_area("Como você quer que seja sua história?", 
                              placeholder="Descreva detalhes: 'Quero que comece em uma floresta...'")
    
    modelo = st.selectbox("Estilo de Escrita", ["📖 Narrativa Longa", "💖 Romance", "🔥 Ação"])

    if st.button("Gerar Primeiro Capítulo ✨"):
        if fandom and titulo and prompt_user:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.prompt_inicial = prompt_user
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Preencha todos os campos!")

# 6. PÁGINA DE CHAT
else:
    st.markdown(f"<h2 style='text-align:center; color:#7d33ff;'>{st.session_state.titulo}</h2>", unsafe_allow_html=True)
    
    # Exibir Chat
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Lógica da IA Groq
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt_sistema = f"Você é o ChatFic AI. Universo: {st.session_state.fandom}. Instrução: {st.session_state.prompt_inicial}. Escreva o Capítulo 1 de forma longa e imersiva."
                
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": prompt_sistema}]
                )
                
                resposta = chat_completion.choices[0].message.content
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error("Configure sua GROQ_API_KEY nos Secrets do Streamlit!")

    # Input contínuo
    if prompt := st.chat_input("Continue a história..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
