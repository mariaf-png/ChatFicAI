import streamlit as st
from groq import Groq
import time

# 1. SETUP: MODO CLARO E MENU DE 3 BARRINHAS
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="collapsed" # Isso garante que as 3 barrinhas apareçam no topo
)

# 2. CSS PARA DESIGN IDÊNTICO (MODO CLARO + ROXO)
st.markdown("""
    <style>
    /* Fundo Claro e Texto Escuro */
    .stApp {
        background-color: #f8f9fa !important;
        color: #212529 !important;
    }
    
    /* Barra Lateral (Configurações) */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #7d33ff !important;
    }

    /* Esconder elementos desnecessários */
    header, footer, .stDeployButton { visibility: hidden !important; }

    /* Logo Animado */
    .app-logo {
        font-size: 60px;
        text-align: center;
        animation: pulse 2s infinite;
        margin-bottom: 10px;
    }
    @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.1);} 100% {transform: scale(1);} }

    /* Balões de Chat (Modo Claro) */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: #f0e6ff !important; /* Roxo bem clarinho */
        border: 1px solid #7d33ff !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
    }

    /* Botão de Enviar Roxo */
    .stChatInput button { background-color: #7d33ff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONTROLE DE PÁGINA E MEMÓRIA
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (MENU DE 3 BARRINHAS)
with st.sidebar:
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>ChatFic AI</h2>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("👤 Minha Conta")
    st.button("Login / Cadastro", use_container_width=True)
    
    st.subheader("⚙️ Aparência")
    st.selectbox("Fonte", ["Inter", "Serif", "Monospace"])
    st.slider("Tamanho da Letra", 14, 28, 18)
    
    st.divider()
    if st.button("➕ Nova Fanfic", use_container_width=True):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 4. PÁGINA INICIAL (COM CAIXA DE PROMPT)
if st.session_state.page == "home":
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #7d33ff;'>ChatFic AI</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Harry Potter")
    with col2:
        titulo = st.text_input("Título da História", placeholder="Ex: A Pedra Filosofal 2")
    
    # CAIXA DE DIÁLOGO PARA O PROMPT INICIAL (COMO QUER A HISTÓRIA)
    prompt_inicial = st.text_area("Como você quer que seja a sua história?", 
                                placeholder="Descreva detalhes: 'Quero que comece em uma floresta, com muito suspense e que o protagonista seja misterioso...'")
    
    modelo = st.selectbox("Estilo de Escrita", ["📖 Narrativa Longa", "💖 Romance", "🔥 Ação", "🎭 Drama"])

    if st.button("Gerar Primeira Cena ✨", use_container_width=True):
        if fandom and titulo and prompt_inicial:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.instrucao_user = prompt_inicial
            st.session_state.modelo = modelo
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Preencha todos os campos para começar!")

# 5. PÁGINA DE CHAT (LÓGICA E IA)
else:
    st.markdown(f"### 🖋️ {st.session_state.titulo} | {st.session_state.fandom}")
    
    # Exibe Histórico
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            st.caption("📋 Copiar | ✂️ Editar | 🔄 Refazer")

    # Primeiro Capítulo Automático (baseado no prompt da home)
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("📖 *Criando primeiro capítulo...*")
            
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            system_prompt = f"""
            Você é o ChatFic AI. Universo: {st.session_state.fandom}. Estilo: {st.session_state.modelo}.
            INSTRUÇÃO DO USUÁRIO: {st.session_state.instrucao_user}
            Escreva o primeiro capítulo de forma longa, humana e emocionante. Inicie com 'Capítulo 1: [Título]'.
            """
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_prompt}]
            )
            
            output = res.choices[0].message.content
            placeholder.markdown(output)
            st.session_state.messages.append({"role": "assistant", "content": output})

    # Próximos passos do chat
    if user_input := st.chat_input("O que acontece agora?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            placeholder = st.empty()
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": f"Continue a fanfic no universo {st.session_state.fandom}. Seja fiel aos detalhes."}] + st.session_state.messages[-10:]
            )
            
            final_res = response.choices[0].message.content
            placeholder.markdown(final_res)
            st.session_state.messages.append({"role": "assistant", "content": final_res})
