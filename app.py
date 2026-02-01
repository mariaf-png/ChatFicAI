import streamlit as st
from groq import Groq
import time
from io import BytesIO
from reportlab.pdfgen import canvas

# 1. CONFIGURAÇÃO INICIAL E ESTILO (UI/UX DEEPSEEK STYLE)
st.set_page_config(page_title="ChatFic AI", page_icon="📖", layout="wide")

# CSS Avançado para Animações, Temas e Layout
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0e0616;
        color: #e0e0e0;
    }

    /* Animação do Livro no Início */
    @keyframes pulse {
        0% { transform: scale(1); filter: drop-shadow(0 0 5px #7d33ff); }
        50% { transform: scale(1.1); filter: drop-shadow(0 0 20px #7d33ff); }
        100% { transform: scale(1); filter: drop-shadow(0 0 5px #7d33ff); }
    }
    .app-logo { font-size: 50px; animation: pulse 2s infinite; text-align: center; }

    /* Estilo DeepSeek Chat Input */
    .stChatInputContainer { padding: 20px; background: transparent !important; }
    .stChatInput input {
        background-color: #1e0f33 !important;
        border: 1px solid #7d33ff !important;
        border-radius: 15px !important;
        color: white !important;
    }

    /* Esconder elementos nativos */
    header, footer, .stDeployButton {display: none !important;}

    /* Botões de Ação na Mensagem (Sutis) */
    .message-tools {
        display: flex; gap: 10px; font-size: 0.8rem; margin-top: 5px; opacity: 0.6;
    }
    .message-tools:hover { opacity: 1; }
    
    /* Indicador de Escrita (Dots) */
    .typing { display: flex; gap: 5px; padding: 10px; }
    .dot { width: 8px; height: 8px; background: #7d33ff; border-radius: 50%; animation: blink 1.4s infinite; }
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0%, 100% { opacity: 0.3; } 50% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. ESTADO DO SISTEMA (MEMÓRIA E CONFIGURAÇÕES)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"
if "theme" not in st.session_state:
    st.session_state.theme = "Escuro"
if "chat_config" not in st.session_state:
    st.session_state.chat_config = {"font_size": 16, "font_family": "Inter", "language": "Português"}

# Funções de utilidade
def export_pdf(text):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, "ChatFic AI - Sua Fanfic")
    p.showPage()
    p.save()
    return buffer.getvalue()

# 3. BARRA LATERAL (CONFIGURAÇÕES, LOGIN, CUSTOMIZAÇÃO)
with st.sidebar:
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.title("ChatFic AI")
    
    with st.expander("👤 Conta"):
        st.text_input("Usuário")
        st.text_input("Senha", type="password")
        st.button("Login / Cadastrar")

    with st.expander("⚙️ Personalização"):
        st.session_state.theme = st.selectbox("Tema", ["Escuro", "Claro"])
        st.session_state.chat_config["language"] = st.selectbox("Idioma", ["Português", "English", "Español"])
        st.session_state.chat_config["font_size"] = st.slider("Tamanho da Fonte", 12, 24, 16)
        st.session_state.chat_config["font_family"] = st.selectbox("Fonte", ["Inter", "Monospace", "Serif"])

    if st.button("➕ Nova Fanfic", use_container_width=True):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

    if st.button("🗑️ Apagar Chat atual"):
        st.session_state.messages = []
        st.rerun()

# 4. PÁGINA INICIAL (ESTILO DEEPSEEK)
if st.session_state.page == "home":
    st.markdown('<div class="app-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Como vamos começar sua história?</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        titulo = st.text_input("Título da Fanfic", placeholder="Ex: O Retorno do Rei")
    with col2:
        fandom = st.text_input("Universo/Fandom", placeholder="Ex: Harry Potter, Marvel...")
    
    st.markdown("### Escolha um Modelo de Escrita")
    modelos = {
        "📖 Narrativa Épica": "Focada em grandes acontecimentos e mundos vastos.",
        "💖 Romance Slow Burn": "Desenvolvimento lento e emocional dos personagens.",
        "🔪 Suspense/Angst": "Tensão alta, drama e mistério.",
        "🎭 Diálogos Intensos": "Foco total na interação e falas dos personagens."
    }
    
    escolha = st.selectbox("Modelos disponíveis:", list(modelos.keys()))
    
    if st.button("Começar a escrever agora"):
        st.session_state.fandom_atual = fandom
        st.session_state.titulo_atual = titulo
        st.session_state.modelo_selecionado = escolha
        st.session_state.page = "chat"
        st.rerun()

# 5. ÁREA DE CHAT (LÓGICA E INTERFACE)
elif st.session_state.page == "chat":
    # Cabeçalho com Opções (Três Pontinhos)
    head_col1, head_col2 = st.columns([0.9, 0.1])
    with head_col1:
        st.subheader(f"📖 {st.session_state.titulo_atual} | {st.session_state.fandom_atual}")
    with head_col2:
        with st.popover("⋮"):
            if st.button("📥 Salvar PDF"):
                st.download_button("Baixar PDF", export_pdf(str(st.session_state.messages)), "fanfic.pdf")
            if st.button("📝 Salvar Markdown"):
                st.download_button("Baixar MD", str(st.session_state.messages), "fanfic.md")
            st.button("🌐 Publicar na Comunidade")

    # Exibir Mensagens
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(f'<div style="font-size: {st.session_state.chat_config["font_size"]}px;">{msg["content"]}</div>', unsafe_allow_html=True)
            
            # Ferramentas de Mensagem (Editar, Copiar, Apagar)
            st.markdown(f"""
                <div class="message-tools">
                    <span>✂️ Editar</span> | <span>📋 Copiar</span> | <span>🗑️ Apagar</span>
                </div>
            """, unsafe_allow_html=True)

    # Input do Usuário
    if prompt := st.chat_input("Continue o capítulo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Indicador de Escrita Animado
            placeholder = st.empty()
            placeholder.markdown('<div class="typing"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>', unsafe_allow_html=True)
            
            # Lógica da IA (Groq)
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Prompt de Sistema Robusto para Memória e Coerência
            instrucao = f"""
            Você é o ChatFic AI. Escreva de forma humana, natural, rápida e animada.
            CONTEXTO: Fanfic do universo {st.session_state.fandom_atual}. 
            ESTILO: {st.session_state.modelo_selecionado}.
            REGRAS:
            1. Capítulos longos e consistentes. Comece com 'Capítulo X: Título do Capítulo'.
            2. Memória impecável: mantenha coerência total com o fandom e fatos anteriores.
            3. Evite repetições de palavras.
            4. Se solicitado 'escrever de novo mas com símbolos', use emojis e caracteres especiais para decorar.
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instrucao}] + st.session_state.messages
            )
            
            full_response = response.choices[0].message.content
            
            # Efeito de Digitação Humana
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text + "▌")
                time.sleep(0.001) # Velocidade rápida como pedido
            
            placeholder.markdown(typed_text)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
