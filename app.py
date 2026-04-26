import streamlit as st
import pandas as pd
import sqlite3
import datetime
import random

# ==============================================================================
# 1. DATABASE ENGINE (O Coração do Sistema)
# ==============================================================================

class LogiflowDB:
    def __init__(self, db_name="logiflow_pro.db"):
        self.db_name = db_name
        self._setup_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _setup_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        # Tabela de Usuários/Vendedores
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            store_name TEXT,
                            address TEXT,
                            is_seller BOOLEAN)''')
        
        # Tabela de Produtos (Catálogo Mestre)
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_name TEXT,
                            category TEXT,
                            is_perishable BOOLEAN)''')

        # Tabela de Inventário (O que está nas prateleiras)
        cursor.execute('''CREATE TABLE IF NOT敎 inventory (
                            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER,
                            seller_id INTEGER,
                            quantity INTEGER,
                            price REAL,
                            expiry_date DATE,
                            location TEXT,
                            address TEXT,
                            is_producer BOOLEAN,
                            last_updated TIMESTAMP,
                            FOREIGN KEY(product_id) REFERENCES products(product_id),
                            FOREIGN KEY(seller_id) REFERENCES users(user_id))''')

        # Tabela de Chat (A Ponte de Comunicação)
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sender_id INTEGER,
                            receiver_id INTEGER,
                            message TEXT,
                            timestamp TIMESTAMP)''')
        
        # Seed inicial de produtos se estiver vazio
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            products = [
                ("Organic Milk", "Dairy", 1), ("Fresh Avocado", "Produce", 1),
                ("Greek Yogurt", "Dairy", 1), ("Sourdough Bread", "Bakery", 1),
                ("Canned Beans", "Pantry", 0), ("Apple", "Produce", 1)
            ]
            cursor.executemany("INSERT INTO products (product_name, category, is_perishable) VALUES (?,?,?)", products)
        
        conn.commit()
        conn.close()

    def query(self, sql, params=()):
        conn = self._get_conn()
        df = pd.read_sql_query(sql, conn, params=params)
        conn.close()
        return df

    def execute(self, sql, params=()):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        conn.close()

# Inicialização Global
db = LogiflowDB()

# ==============================================================================
# 2. LOGIC ENGINE (A Inteligência do Sistema)
# ==============================================================================

class LogiflowAgent:
    @staticmethod
    def get_ai_suggestions(user_id):
        """Simula a IA analisando o estoque do vendedor para sugerir ações."""
        conn = db._get_conn()
        df = pd.read_sql_query("SELECT * FROM inventory WHERE seller_id = ?", conn, params=(user_id,))
        conn.close()
        
        suggestions = []
        today = datetime.date.today()
        for _, row in df.iterrows():
            expiry = pd.to_datetime(row['expiry_date']).date()
            if (expiry - today).days < 3:
                suggestions.append(f"⚠️ {row['product_id']} está vencendo! Sugestão: Aplicar 50% de desconto.")
            if row['quantity'] < 5:
                suggestions.append(f"📉 {row['product_id']} está com estoque baixo! Sugestão: Repor agora.")
        return suggestions

# ==============================================================================
# 3. USER INTERFACE (O Dashboard Profissional)
# ==============================================================================

def main():
    st.set_page_config(page_title="Logiflow Bridge", layout="wide")
    
    # Estilo CSS para parecer um App Mobile/Web moderno
    st.markdown("""
        <style>
        .main { background-color: #f4f7f6; }
        .stButton>button { width: 100%; border-radius: 8px; }
        .card { padding: 20px; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    # Gerenciamento de Sessão (Simulando Login)
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
        st.session_state.role = None

    # --- SIDEBAR: NAVEGAÇÃO ---
    st.sidebar.title("🌿 Logiflow")
    if st.session_state.user_id is None:
        mode = st.sidebar.selectbox("Entrar como:", ["Consumidor", "Vendedor"])
        if st.sidebar.button("Login / Iniciar"):
            if mode == "Consumidor":
                st.session_state.role = "user"
                st.session_state.user_id = 999 # ID genérico para cliente
            else:
                st.session_state.role = "seller"
                # Simulação de cadastro rápido de vendedor
                st.session_state.user_id = 1 
                st.session_state.store_name = "Minha Fazenda Local"
            st.rerun()
    else:
        st.sidebar.write(f"👤 Modo: {st.session_state.role.capitalize()}")
        if st.sidebar.button("Sair"):
            st.session_state.user_id = None
            st.rerun()

    # --- LÓGICA DE TELAS ---

    if st.session_state.user_id is None:
        st.title("Bem-vindo ao Logiflow")
        st.info("Por favor, selecione seu perfil na barra lateral para começar.")
        st.image("https://img.freepik.com/free-vector/logistics-concept-illustration_114360-1001.jpg", width=400)

    elif st.session_state.role == "user":
        render_user_view()

    elif st.session_state.role == "seller":
        render_seller_view()

# --- TELAS ESPECÍFICAS ---

def render_user_view():
    st.title("🛒 Marketplace Local")
    
    # 1. Busca Inteligente
    query = st.text_input("O que você deseja encontrar hoje?", placeholder="Ex: Milk, Avocado...")
    
    if query:
        results = db.search_items(query)
        if results.empty:
            st.warning("Nenhum produto encontrado.")
        else:
            st.write(f"Encontramos {len(results)} itens para você:")
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: white; margin-bottom: 10px;">
                        <div style="font-size: 18px; font-weight: bold;">{row['name']}</div>
                        <div style="color: #27ae60;">{'🌿 PRODUTOR LOCAL' if row['is_producer'] else ''}</div>
                        <div style="font-size: 16px; color: #2c3e50;">Preço: ${row['price']:.2f}</div>
                        <div style="font-size: 12px; color: #7f8c8d;">📍 {row['location']} | {row['address']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"💬 Chat com {row['store_name']}", key=f"chat_{row['item_id']}"):
                        st.info(f"Iniciando chat com {row['store_name']}... (Simulação)")

def render_seller_view():
    st.title("🏪 Painel do Vendedor")
    
    # 2. IA Decision Queue (O diferencial do seu projeto)
    st.subheader("🤖 Sugestões da IA (Co-Pilot)")
    suggestions = LogiflowAgent().run_ai_analysis()
    if not suggestions:
        st.success("Tudo em ordem! Nenhuma ação urgente necessária.")
    else:
        for i, sug in enumerate(suggestions):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.warning(f"**{sug['reason']}** ({sug['name']})")
            with col2:
                if st.button("Autorizar", key=f"auth_{i}"):
                    LogiflowAgent().authorize_action(i)
                    st.rerun()

    st.write("---")

    # 3. Gestão de Estoque
    tab1, tab2 = st.tabs(["📦 Meu Estoque", "➕ Novo Cadastro"])
    
    with tab1:
        st.subheader("Seu Inventário Atual")
        # Filtra estoque apenas do vendedor logado (simulado como ID 1)
        my_stock = db.query("SELECT p.name, i.quantity, i.price, i.expiry_date, i.location FROM inventory i JOIN products p ON i.product_id = p.product_id WHERE i.seller_id = 1")
        st.dataframe(my_stock, use_container_width=True)

    with tab2:
        st.subheader("Cadastrar Novo Item")
        with st.form("add_form"):
            p_name = st.selectbox("Produto", ["Organic Milk", "Fresh Avocado", "Greek Yogurt", "Sourdough Bread", "Canned Beans"])
            qty = st.number_input("Quantidade", min_value=1)
            price = st.number_input("Preço ($)", min_value=0.1)
            exp = st.date_input("Data de Validade")
            loc = st.text_input("Localização (Ex: Prateleira A)")
            addr = st.text_input("Endereço da Loja")
            is_prod = st.checkbox("Sou Produtor Local")
            
            if st.form_submit_button("Publicar no Logiflow"):
                # Busca o ID do produto
                p_id_df = db.query("SELECT product_id FROM products WHERE name = ?", (p_name,))
                if not p_id_df.empty:
                    p_id = p_id_df.iloc[0]['product_id']
                    db.execute("""INSERT INTO inventory (product_id, quantity, location, expiry_date, price, last_updated, discount_pct, address, seller_id, is_producer) 
                                  VALUES (?,?,?,?,?,?,?,?,?,?)""", 
                               (p_id, qty, loc, exp.isoformat(), price, datetime.datetime.now(), 0.0, addr, 1, is_prod))
                    st.success("Produto cadastrado e visível para clientes!")
                else:
                    st.error("Produto não encontrado no catálogo.")

if __name__ == "__main__":
    main()
