import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO E MENU (AS 3 BARRINHAS)
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Deixa as 3 barrinhas visíveis no topo
)

# 2. CSS PARA O SEU VISUAL (ROXO NEON)
st.markdown("""
    <style>
    .stApp { background: #0e0616; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #1a0b2e !important; border-right: 2px solid #9d4edd; }
    header, footer { visibility: hidden !important; }
    
    /* Animação do Livro */
    .logo-anime { font-size: 50px; text-align: center; animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
    
    /* Balões de Chat */
    .stChatMessage { border-radius: 20px !important; border: 1px solid #3c165a !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE MEMÓRIA
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# 4. BARRA LATERAL (CONFIGURAÇÕES)
with st.sidebar:
    st.markdown('<div class="logo-anime">📖</div>', unsafe_allow_html=True)
    st.title("ChatFic AI")
    st.divider()
    with st.expander("👤 Conta"):
        st.button("Login / Cadastro", use_container_width=True)
    with st.expander("⚙️ Ajustes"):
        st.selectbox("Fonte", ["Inter", "Serif", "Monospace"])
        st.slider("Tamanho", 14, 24, 16)
    st.divider()
    if st.button("➕ Nova Fanfic"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 5. NAVEGAÇÃO ENTRE PÁGINAS
if st.session_state.page == "home":
    # PÁGINA INICIAL
    st.markdown("<h1 style='text-align: center; color: #9d4edd;'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Insira o título e o universo para começar.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fandom = st.text_input("Qual o Fandom / Universo?")
    with c2:
        titulo = st.text_input("Título da História")
    
    modelo = st.selectbox("Estilo de Escrita ✍️", ["📖 Épico", "💖 Romance", "🔥 Ação", "🎭 Drama"])
    
    if st.button("Criar Fanfic Agora ✨", use_container_width=True):
        if fandom and titulo:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.modelo = modelo
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Preencha o Fandom e o Título!")

else:
    # PÁGINA DE CHAT
    st.markdown(f"### 📖 {st.session_state.titulo}")
    
    # Exibe Histórico
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Entrada de texto
    if prompt := st.chat_input("Continue a história..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("📖 *ChatFic está escrevendo...*")
            
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Memória: enviamos o contexto para a IA
            instrucao = f"Você é o ChatFic AI. Universo: {st.session_state.fandom}. Estilo: {st.session_state.modelo}. Escreva capítulos longos, coerentes e naturais. Inicie com 'Capítulo X: Título'."
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instrucao}] + st.session_state.messages[-10:]
            )
            
            final_txt = res.choices[0].message.content
            placeholder.markdown(final_txt)
            st.session_state.messages.append({"role": "assistant", "content": final_txt})
            
