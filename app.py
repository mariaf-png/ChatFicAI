import streamlit as st
from groq import Groq
import time

# 1. SETUP DE LAYOUT (FORÇA O MENU LATERAL)
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. CSS PARA CLONAR O SEU APP (TUDO IGUAL)
st.markdown("""
    <style>
    /* Fundo Roxo Escuro Original */
    .stApp {
        background: #0e0616 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Customizando a Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #1a0b2e !important;
        border-right: 2px solid #9d4edd !important;
    }

    /* Esconder elementos nativos do Streamlit */
    header, footer, .stDeployButton { visibility: hidden !important; }

    /* Logo Animado (Livro) */
    .app-logo {
        font-size: 70px;
        text-align: center;
        animation: float 3s ease-in-out infinite;
        margin-top: 20px;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }

    /* Balões de Chat Idênticos ao seu site */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        border: 1px solid #3c165a !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: #3c165a !important;
        margin-left: 20% !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: #1e0f33 !important;
        border-color: #9d4edd !important;
        margin-right: 20% !important;
    }

    /* Ícones de Copiar e Editar sutilmente abaixo das mensagens */
    .msg-actions {
        font-size: 0.8rem;
        color: #9d4edd;
        margin-top: 5px;
        display: flex;
        gap: 15px;
        cursor: pointer;
    }

    /* Input de Chat Estilizado */
    .stChatInputContainer {
        padding: 10px 10% !important;
        background: transparent !important;
    }
    .stChatInput input {
        border: 2px solid #9d4edd !important;
        background: #1a0b2e !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Indicador de Digitação (Dots) */
    .typing-indicator {
        display: flex; gap: 4px; padding: 10px;
    }
    .dot { width: 6px; height: 6px; background: #9d4edd; border-radius: 50%; animation: blink 1.4s infinite; }
    @keyframes blink { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE NAVEGAÇÃO E MEMÓRIA
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (ACESSÍVEL PELO MENU DE 3 BARRINHAS NO TOPO)
with st.sidebar:
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>ChatFic AI</h2>", unsafe_allow_html=True)
    st.divider()
    
    with st.expander("👤 Conta"):
        st.button("Login", use_container_width=True)
        st.button("Cadastrar", use_container_width=True)
    
    with st.expander("⚙️ Preferências"):
        st.selectbox("Fonte do Chat", ["Inter", "Serif", "Monospace"])
        st.slider("Tamanho da Fonte", 14, 28, 18)
        st.selectbox("Idioma", ["Português", "English"])

    st.divider()
    if st.button("✨ Nova Fanfic / Limpar", use_container_width=True):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# 4. PÁGINA INICIAL (IDÊNTICA AO SEU SITE)
if st.session_state.page == "home":
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #9d4edd;'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A inteligência artificial fiel ao seu fandom.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fandom = st.text_input("Qual o Universo/Fandom?", placeholder="Ex: Marvel")
    with c2:
        titulo = st.text_input("Título da História", placeholder="Ex: O Legado de Asgard")
    
    modelo = st.selectbox("Escolha seu Estilo de Escrita ✍️", [
        "📖 Narrativa Longa e Humana", "💕 Romance Slow Burn", "🔥 Ação e Aventura", "🎭 Foco em Diálogos"
    ])

    if st.button("Começar a Escrever ✨", use_container_width=True):
        if fandom and titulo:
            st.session_state.fandom = fandom
            st.session_state.titulo = titulo
            st.session_state.modelo = modelo
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.error("Preencha o Título e o Universo primeiro!")

# 5. PÁGINA DE CHAT (LÓGICA E SERVIDOR)
else:
    # Topo com Opções (Três Pontinhos)
    col_t1, col_t2 = st.columns([0.9, 0.1])
    with col_t1:
        st.markdown(f"### 🖋️ {st.session_state.titulo} | {st.session_state.fandom}")
    with col_t2:
        with st.popover("⋮"):
            st.button("📥 PDF")
            st.button("📝 Markdown")
            st.button("🗑️ Apagar")

    # Mostrar Histórico (Memória Ativa)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            st.markdown('<div class="msg-actions">📋 Copiar | ✂️ Editar | 🔄 Refazer</div>', unsafe_allow_html=True)

    # Entrada de Texto
    if prompt := st.chat_input("Diga o que acontece a seguir na fanfic..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown('<div class="typing-indicator"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
            
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Memória da IA focada no Fandom e na Coerência
            instrucoes = f"""
            Você é o ChatFic AI. Universo: {st.session_state.fandom}. Estilo: {st.session_state.modelo}.
            REGRAS: Escreva capítulos LONGOS e naturais. Use 'Capítulo X: Título'. 
            Evite repetições. Tenha memória absoluta dos fatos anteriores.
            Seja 100% fiel ao fandom {st.session_state.fandom}.
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instrucoes}] + st.session_state.messages[-15:]
            )
            
            full_response = completion.choices[0].message.content
            
            # Efeito de Digitação
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text + "▌")
                time.sleep(0.005)
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
