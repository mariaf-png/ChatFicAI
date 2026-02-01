import streamlit as st
import streamlit as st
from groq import Groq
import time

# 1. CONFIGURAÇÃO DE LAYOUT FORÇADA
st.set_page_config(
    page_title="ChatFic AI", 
    page_icon="📖", 
    layout="wide", 
    initial_sidebar_state="expanded" # Isso força a barra lateral a abrir
)

# 2. CSS PARA CLONAR O DEEPSEEK (ROXO NEON E DARK MODE)
st.markdown("""
    <style>
    /* Forçar fundo e cores do DeepSeek */
    .stApp {
        background: #0e0616 !important;
        color: #e0e0e0 !important;
    }
    
    /* Forçar visibilidade da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #160a25 !important;
        border-right: 2px solid #7d33ff !important;
        min-width: 260px !important;
    }

    /* Animação do Livro */
    @keyframes pulse-book {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(5deg) scale(1.1); }
        100% { transform: rotate(0deg) scale(1); }
    }
    .book-logo { 
        font-size: 60px; 
        display: block; 
        margin: auto; 
        animation: pulse-book 2s infinite; 
    }

    /* Chat Input igual ao DeepSeek */
    .stChatInputContainer {
        border-top: 1px solid #7d33ff !important;
        background: #0e0616 !important;
    }
    
    /* Esconder botões padrão que estragam o visual */
    header, footer, .stDeployButton { visibility: hidden !important; height: 0 !important; }

    /* Estilo dos balões de chat */
    .stChatMessage { border-radius: 15px !important; padding: 15px !important; margin: 10px 0 !important; }
    .stChatMessage[data-testid="stChatMessageUser"] { background: #2d1b4d !important; border: 1px solid #5a2bb0 !important; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { background: #1e0f33 !important; border: 1px solid #7d33ff !important; }

    /* Três pontinhos animados */
    .typing-dot {
        width: 6px; height: 6px; background: #7d33ff; border-radius: 50%;
        display: inline-block; animation: wave 1.3s linear infinite;
    }
    @keyframes wave { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-5px); } }
    </style>
    """, unsafe_allow_html=True)

# --- INÍCIO DA LÓGICA ---

if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "home"

# BARRA LATERAL (SIDEBAR) - O "NEGÓCIO DO LADO"
with st.sidebar:
    st.markdown('<div class="book-logo">📖</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>ChatFic AI</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    # LOGIN E CADASTRO
    with st.expander("👤 Conta & Acesso"):
        st.text_input("E-mail")
        st.text_input("Senha", type="password")
        st.button("Entrar", use_container_width=True)
    
    # CONFIGURAÇÕES DO CHAT
    with st.expander("⚙️ Preferências"):
        st.selectbox("Tema", ["Escuro 🌙", "Claro ☀️"])
        st.slider("Tamanho da Letra", 12, 24, 16)
        st.selectbox("Fonte", ["Inter", "Arial", "Courier New"])
    
    st.divider()
    if st.button("➕ Nova Fanfic", use_container_width=True):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()

# PÁGINA INICIAL (ESTILO DEEPSEEK)
if st.session_state.page == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color:#7d33ff;'>ChatFic AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Insira o universo e o título para começar a sua obra prima.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fandom = st.text_input("Qual o Fandom / Universo?", placeholder="Ex: Percy Jackson")
    with c2:
        titulo = st.text_input("Título da História", placeholder="Ex: O Herói Perdido")
    
    modelo = st.selectbox("Escolha o Estilo de Escrita ✍️", 
                         ["🏰 Narrativa Épica (Longa)", "💘 Romance Intenso", "👻 Terror Psicológico", "⚔️ Ação e Combate"])
    
    if st.button("Criar Fanfic Agora ✨", use_container_width=True):
        st.session_state.fandom = fandom
        st.session_state.titulo = titulo
        st.session_state.modelo = modelo
        st.session_state.page = "chat"
        st.rerun()

# PÁGINA DE CHAT
else:
    # Topo do Chat (Título e Três Pontinhos)
    t1, t2 = st.columns([0.9, 0.1])
    with t1:
        st.markdown(f"### 📖 {st.session_state.titulo}")
    with t2:
        with st.popover("⋮"):
            st.button("📥 Baixar PDF")
            st.button("📄 Baixar Markdown")
            st.button("🗑️ Apagar Chat")

    # Exibição das Mensagens
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    # Entrada de Texto
    if prompt := st.chat_input("Escreva o próximo passo da história..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("📖 *ChatFic está escrevendo...* <span class='typing-dot'></span><span class='typing-dot'></span>", unsafe_allow_html=True)
            
            # Chama a IA Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            instrucoes = f"Você é o ChatFic AI. Escreva uma fanfic do universo {st.session_state.fandom} com o título {st.session_state.titulo}. Use o modelo {st.session_state.modelo}. Seja humano, use capítulos longos nomeados como 'Capítulo X: Título', evite repetições e seja fiel ao fandom."
            
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": instrucoes}] + st.session_state.messages
            )
            
            final_text = res.choices[0].message.content
            
            # Animação rápida de digitação
            full_txt = ""
            for chunk in final_text.split():
                full_txt += chunk + " "
                placeholder.markdown(full_txt + "▌")
                time.sleep(0.05)
                
            placeholder.markdown(full_txt)
            st.session_state.messages.append({"role": "assistant", "content": final_text})
            
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
