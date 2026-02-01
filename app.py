import streamlit as st

# 1. Configuração da Página
st.set_page_config(page_title="ChatFic AI", layout="centered", initial_sidebar_state="expanded")

# 2. Inicialização Robusta do Estado (Session State)
if "page" not in st.session_state:
    st.session_state.page = "home"

# Funções de Navegação (Callbacks) - Isso garante que o botão funcione sempre
def ir_para_home():
    st.session_state.page = "home"
    st.session_state.messages = []

def ir_para_chat():
    st.session_state.page = "chat"

# 3. CSS para manter o visual das fotos
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* Botões da Sidebar - Roxo e Oval como na Foto 11967 */
    [data-testid="stSidebar"] .stButton button {
        background-color: #5D5FEF !important;
        color: white !important;
        border-radius: 50px !important;
        width: 100% !important;
        border: none !important;
        padding: 10px !important;
    }

    /* Inputs Arredondados como na Foto 11965 */
    .stTextInput input {
        border-radius: 20px !important;
        background-color: #F8F9FB !important;
        border: 1px solid #E6E8EB !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("### 📖 ChatFic")
    # Usamos o parâmetro on_click para garantir que a função seja chamada
    st.button("＋ Nova Fanfic", on_click=ir_para_home)
    
    st.markdown("---")
    st.button("🌍 Comunidade")
    st.button("⚙️ Configurações")

# 5. Lógica de Exibição de Telas
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>Nova Fanfic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Sua próxima obra-prima começa agora.</p>", unsafe_allow_html=True)
    
    titulo = st.text_input("TÍTULO DA SUA OBRA...", placeholder="Dê um nome épico...")
    universo = st.text_input("UNIVERSO (EX: MARVEL, ONE PIECE)", placeholder="Hogwarts, Gotham...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Botão principal também com on_click
    st.button("GERAR HISTÓRIA ✨", on_click=ir_para_chat)

elif st.session_state.page == "chat":
    st.markdown("<h2 style='text-align:center;'>🖋️ Criando sua História</h2>")
    st.info("O chat está pronto para começar!")
    if st.button("← Voltar para o Início", on_click=ir_para_home):
        pass
        
