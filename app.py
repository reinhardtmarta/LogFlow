import streamlit as st
import pandas as pd
import datetime
from logiflow.engine import LogiflowEngine

# Configuração da Página (Mobile First)
st.set_page_config(page_title="Logiflow Bridge", page_icon="🌿", layout="centered")

# Inicialização do Engine (Usando Cache para não recriar o banco toda hora)
@st.cache_resource
def get_engine():
    return LogiflowEngine()

engine = get_engine()

# --- ESTILO CSS CUSTOMIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #27ae60; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    .card { padding: 15px; border-radius: 10px; border: 1px solid #ddd; background: white; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .badge-producer { color: #27ae60; font-weight: bold; font-size: 12px; }
    .badge-warning { color: #e67e22; font-weight: bold; }
    .badge-danger { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: NAVEGAÇÃO ---
st.sidebar.title("Logiflow Menu")
mode = st.sidebar.radio("Escolha seu perfil:", ["🛒 Consumidor (User)", "🏪 Vendedor (Seller)"])

# ==========================================
# MODO 1: CONSUMIDOR (USER)
# ==========================================
if mode == "🛒 Consumidor (User)":
    st.title("🌿 Logiflow Search")
    st.subheader("Encontre produtos frescos perto de você")
    
    query = st.text_input("O que você está procurando?", placeholder="Ex: Milk, Avocado...")
    
    if query:
        results = engine.search_items(query)
        
        if results.empty:
            st.warning("⚠️ Nenhum item encontrado localmente. Tentando conexão global...")
            st.info("🌐 [Clique aqui para ver no Google Shopping](https://www.google.com/shopping)")
        else:
            st.write(f"### Resultados para '{query}':")
            for _, row in results.iterrows():
                # Lógica de Zero Waste
                is_zero_waste = row['discount_pct'] > 0 or (pd.to_datetime(row['expiry_date']).date() - datetime.date.today()).days < 3
                
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size: 14px; color: #27ae60;">{'🌿 LOCAL PRODUCER' if row['is_producer'] else ''}</div>
                        <div style="font-size: 18px; font-weight: bold;">{row['name']}</div>
                        <div style="color: #e67e22; font-weight: bold;">{'🎁 FREE / DONATION' if is_zero_waste else f'${row['price']:.2f}'}</div>
                        <div style="font-size: 12px; color: #7f8c8d;">📍 {row['location']} | {row['address']}</div>
                        <div style="font-size: 10px; color: #e74c3c;">{'🔥 ZERO WASTE DEAL' if is_zero_waste else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# MODO 2: VENDEDOR (SELLER)
# ==========================================
else:
    st.title("🏪 Seller Dashboard")
    st.subheader("Gerencie seu estoque e decisões de IA")

    # --- ABA 1: REGISTRO ---
    with st.expander("➕ Cadastrar Novo Produto", expanded=True):
        with st.form("registration_form"):
            name = st.text_input("Nome do Produto")
            qty = st.number_input("Quantidade", min_value=0, step=1)
            price = st.number_input("Preço ($)", min_value=0.0, step=0.5)
            exp = st.date_input("Data de Validade", datetime.date.today() + datetime.timedelta(days=7))
            loc = st.text_input("Loja/Local", placeholder="Ex: Corner Market")
            addr = st.text_input("Endereço Completo", placeholder="Rua X, nº 123")
            is_prod = st.checkbox("É um Produtor Local?")
            submit = st.form_submit_button("Enviar para Logiflow")

            if submit:
                data = {
                    "name": name, "qty": qty, "pric
