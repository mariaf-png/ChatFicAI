import streamlit as st
from groq import Groq

# 1. CONFIGURAÇÃO DA PÁGINA (MODO CLARO POR PADRÃO)
st.set_page_config(page_title="ChatFic AI", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS AVANÇADO PARA CLONAR A INTERFACE DAS FOTOS
st.markdown("""
    <style>
    /* Fundo Cinza Azulado muito claro (Background das fotos) */
    .stApp {
        background-color: #F8F9FD !important;
        color: #1E1E2D !important;
        font-family: 'Inter', sans-serif;
    }

    /* BARRA LATERAL (SIDEBAR) IDENTICA */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E0E0E0 !important;
    }
    .st-emotion-cache-16idsys p { color: #6E6E80 !important; font-weight: 600; }

    /* CARD DE ENTRADA (Onde fica o título e universo) */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1E1E2D !important;
        border-radius: 20px !important; /* Super arredondado como na foto */
        border: 1px solid #EAEAEA !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
    }

    /* BOTÃO 'NOVA FANFIC' E 'GERAR' (Roxo Vibrante) */
    .stButton button {
        background-color: #5D5FEF !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 24px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: 0.3s;
    }
    .stButton button:hover { background-color: #4A4CCF !important; transform: scale(1.02); }

    /* BARRA DE CHAT FLUTUANTE (Parte de baixo) */
    .stChatInputContainer {
        padding: 10px !important;
        background-color: transparent !important;
    }
    .stChatInput input {
        border-radius: 30px !important;
        border: 1px solid #EAEAEA !important;
        background-color: #FFFFFF !important;
    }

    /* TÍTULOS E TEXTOS */
    h1 { color: #1E1E2D !important; font-weight: 800 !important; text-align: center; }
    .sub-text { color: #8E8E93; text-align: center; margin-bottom: 30px; }

    /* Esconder o menu de desenvolvedor para parecer App nativo */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA LATERAL (MENU)
with st.sidebar:
    st.markdown("### 📖 ChatFic")
    if st.button("＋ Nova Fanfic"):
        st.session_state.messages = []
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("---")
    st.markdown("🌍 **Comunidade**")
    st.markdown("⚙️ **Configurações**")

# 4. LÓGICA DE PÁGINAS
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

# TELA INICIAL (IGUAL À FOTO 11965)
if st.session_state.page == "home":
    st.markdown("<p style='text-align:center; font-size: 60px;'>📖</p>", unsafe_allow_html=True)
    st.markdown("<h1>Nova Fanfic</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>Sua próxima obra-prima começa agora.</p>", unsafe_allow_html=True)

    titulo = st.text_input("TÍTULO DA SUA OBRA...", placeholder="Dê um nome épico...")
    fandom = st.text_input("UNIVERSO (EX: MARVEL, ONE PIECE)", placeholder="Hogwarts, Gotham, Multiverso...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("GERAR HISTÓRIA ✨"):
        if titulo and fandom:
            st.session_state.titulo = titulo
            st.session_state.fandom = fandom
            st.session_state.page = "chat"
            st.rerun()
        else:
            st.warning("Preencha o título e o universo!")

# TELA DE CHAT
else:
    st.markdown(f"<h3 style='text-align:center;'>{st.session_state.titulo}</h3>", unsafe_allow_html=True)
    
    # Exibir mensagens
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Entrada de texto (Barra flutuante)
    if prompt := st.chat_input("O que acontece a seguir na sua história?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                # Contexto da Fanfic para a IA
                system_msg = f"Você é um escritor de fanfics. Título: {st.session_state.titulo}. Universo: {st.session_state.fandom}."
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
                )
                full_res = response.choices[0].message.content
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error("Erro na API Groq. Verifique sua chave nos Secrets.")
                
