import streamlit as st
import pandas as pd
import datetime
import random
import sqlite3
import sys

# Importando o seu motor de lógica
# Certifique-se de que a pasta 'logiflow' está no mesmo diretório que este app.py
try:
    from logiflow.engine import LogiflowEngine
except ImportError:
    # Caso você esteja rodando de forma isolada para teste
    from main import LogiflowEngine 

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Logiflow Bridge", page_icon="🌿", layout="centered")

# Inicialização do Engine (Cache para não recriar o banco toda hora)
@st.cache_resource
def get_engine():
    return LogiflowEngine()

engine = get_engine()

# --- CSS CUSTOMIZADO PARA O LOOK PROFISSIONAL ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #27ae60; color: white; }
    .card { padding: 15px; border-radius: 10px; border: 1px solid #ddd; background: white; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. INTERFACE DO USUÁRIO (CONSUMIDOR)
# ==============================================================================

def render_user_portal():
    st.title("🛒 User Search Portal")
    st.subheader("Encontre produtos frescos perto de você")
    
    query = st.text_input("O que você está procurando?", placeholder="Ex: Milk, Avocado...")
    
    if query:
        results = engine.search_items(query)
        
        if results.empty:
            st.warning("⚠️ Nenhum item encontrado localmente.")
        else:
            st.write(f"### Resultados para '{query}':")
            for _, row in results.iterrows():
                # Lógica de Zero Waste
                is_zero_waste = row['discount_pct'] > 0 or (pd.to_datetime(row['expiry_date']).date() - datetime.date.today()).days < 3
                badge = "🌿 <b>LOCAL FARMER</b>" if row['is_producer'] else ""
                price_text = "🎁 <b>FREE (DONATION)</b>" if is_zero_waste else f"${row['price']:.2f}"
                
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 11px; color: #27ae60;">{badge}</div>
                    <div style="font-size: 18px; font-weight: bold;">{row['name']}</div>
                    <div style="font-size: 16px; color: #e67e22;">{price_text}</div>
                    <div style="font-size: 12px; color: #7f8c8d;">📍 {row['location']} | {row['address']}</div>
                    <div style="font-size: 10px; color: #e74c3c; font-weight: bold;">{'🔥 ZERO WASTE DEAL' if is_zero_waste else ''}</div>
                </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# 3. INTERFACE DO VENDEDOR (SELLER)
# ==============================================================================

def render_seller_portal():
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
            addr = st.text_input("Endereço Completo", placeholder="123 Main St")
            is_prod = st.checkbox("É um Produtor Local?")
            submit = st.form_submit_button("Enviar para Logiflow")

            if submit:
                if not name or not loc or not addr:
                    st.error("Por favor, preencha todos os campos.")
                else:
                    data = {
                        "name": name, "qty": qty, "price": price, "exp": exp,
                        "loc": loc, "addr": addr, "last_upd": datetime.datetime.now(),
                        "is_prod": is_prod
                    }
                    success, msg = engine.register_item(data)
                    if success: st.success(msg)
                    else: st.error(msg)

    # --- ABA 2: DECISÕES DA IA ---
    st.write("---")
    st.subheader("🤖 AI Decision Queue")
    proposals = engine.run_ai_analysis()
    
    if not proposals:
        st.info("Nenhuma ação pendente da IA.")
    else:
        for i, p in enumerate(proposals):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.warning(f"**{p['type']}**: {p['name']} ({p['reason']})")
            with col2:
                if st.button(f"Approve", key=f"app_{i}"):
                    engine.authorize_action(i)
                    st.rerun()

    # --- ABA 3: IMPACTO ---
    st.write("---")
    st.subheader("📊 Impacto Social")
    c1, c2, c3 = st.columns(3)
    c1.metric("Waste Prevented", "12 items")
    c2.metric("Donations", "4 items")
    c3.metric("Merchant Savings", "$45.50")

# ==========================================
# 4. MAIN APP ROUTING
# ==========================================

def main():
    st.sidebar.title("Logiflow Menu")
    mode = st.sidebar.radio("Escolha seu perfil:", ["🛒 Consumidor (User)", "🏪 Vendedor (Seller)"])

    if mode == "🛒 Consumidor (User)":
        render_user_portal()
    else:
        render_seller_portal()

if __name__ == "__main__":
    main()
