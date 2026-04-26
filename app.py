import streamlit as st
import pandas as pd
import datetime
import json
import os

# ==============================================================================
# 1. DATA MANAGER (JSON-based - Sem erros de trava de banco)
# ==============================================================================

class LogiflowData:
    def __init__(self, filename="logiflow_data.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        else:
            # Dados iniciais para o protótipo não começar vazio
            return {
                "inventory": [
                    {"id": 1, "name": "Organic Milk", "store": "Corner Market", "price": 4.50, "qty": 10, "expiry": "2024-05-25", "producer": True, "address": "123 Main St"},
                    {"id": 2, "name": "Fresh Avocado", "store": "Green Grocer", "price": 2.0, "qty": 5, "expiry": "2024-05-20", "producer": True, "address": "45 Farm Rd"},
                    {"id": 3, "name": "Canned Beans", "store": "City Mart", "price": 1.5, "qty": 50, "expiry": "2025-12-01", "producer": False, "address": "99 Central Ave"}
                ],
                "chats": [] # Histórico de conversas
            }

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_item(self, item):
        self.data['inventory'].append(item)
        self.save()

    def update_stock(self, product_name, store_name, qty, price, expiry, address, is_producer):
        # Procura se o item já existe para atualizar (Upsert)
        for item in self.data['inventory']:
            if item['name'] == product_name and item['store'] == store_name:
                item.update({
                    "qty": qty, "price": price, "expiry": expiry, 
                    "address": address, "is_producer": is_producer
                })
                self.save()
                return True
        
        # Se não existe, cria novo
        new_item = {
            "id": len(self.data['inventory']) + 1,
            "name": product_name, "qty": qty, "store": store_name,
            "price": price, "expiry": expiry, "address": address,
            "is_producer": is_producer
        }
        self.add_item(new_item)
        return True

    def add_chat_message(self, user, message):
        self.data['chats'].append({
            "timestamp": datetime.datetime.now().strftime("%H:%M"),
            "user": user,
            "text": message
        })
        self.save()

# Inicializa o motor
db = LogiflowData()

# ==============================================================================
# 2. INTERFACE (Streamlit - Mobile Friendly)
# ==============================================================================

st.set_page_config(page_title="Logiflow Bridge", page_icon="🌿")

# CSS para deixar com cara de App
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .chat-bubble { padding: 10px; border-radius: 15px; margin: 5px 0; font-family: sans-serif; }
    .user-msg { background-color: #e1f5fe; text-align: right; }
    .seller-msg { background-color: #f1f1f1; text-align: left; }
    .card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar de Navegação
st.sidebar.title("🌿 Logiflow")
mode = st.sidebar.radio("Acesse como:", ["🛒 Consumidor (User)", "🏪 Vendedor (Seller)"])

# ==============================================================================
# 3. MODO CONSUMIDOR (Busca estilo Google + Chat)
# ==============================================================================

if mode == "🛒 Consumidor (User)":
    st.title("Find Local Goods")
    st.write("Search for products and chat directly with sellers.")

    query = st.text_input("🔍 What are you looking for?", placeholder="e.g. Milk")

    if query:
        # Simulação de busca "Google-style"
        results = [i for i in db.data['inventory'] if query.lower() in i['name'].lower()]
        
        if not results:
            st.error("No local stock found. Redirecting to Global Shopping...")
            st.markdown("[🌐 View on Google Shopping](https://www.google.com/shopping)")
        else:
            for item in results:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <div style="font-size: 18px; font-weight: bold;">{item['name']}</div>
                        <div style="color: #27ae60;">{'🌿 LOCAL PRODUCER' if item['is_producer'] else ''}</div>
                        <div style="font-size: 16px; color: #2c3e50;">Price: ${item['price']:.2f}</div>
                        <div style="font-size: 14px; color: #7f8c8d;">📍 {item['store']} | {item['address']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Botão de Chat (Simulado)
                    if st.button(f"💬 Chat with {item['store']}", key=f"chat_{item['id']}"):
                        st.session_state['active_chat'] = item['store']
                        st.session_state['chat_history'] = [] # Limpa para o exemplo

    # Se um chat estiver ativo
    if 'active_chat' in st.session_state:
        st.write("---")
        st.subheader(f"💬 Chat with {st.session_state['active_chat']}")
        
        # Exibe histórico (Simulado)
        for msg in st.session_state.get('chat_history', []):
            st.markdown(f"<div class='chat-bubble {msg['type']}'>{msg['text']}</div>", unsafe_allow_html=True)
        
        user_msg = st.text_input("Type your message...", key="chat_input")
        if st.button("Send"):
            if user_msg:
                st.session_state['chat_history'].append({"type": "user-msg", "text": user_msg})
                st.rerun()

# ==============================================================================
# 4. MODO VENDEDOR (Gestão + Cadastro)
# ==============================================================================

else:
    st.title("🏪 Seller Dashboard")
    st.subheader("Manage your local inventory")

    tab1, tab2 = st.tabs(["📦 Inventory Management", "💬 Customer Chats"])

    with tab1:
        with st.expander("➕ Register / Update Product", expanded=True):
            with st.form("seller_form"):
                name = st.text_input("Product Name")
                qty = st.number_input("Quantity", min_value=0)
                price = st.number_input("Price ($)", min_value=0.0, step=0.5)
                exp = st.date_input("Expiry Date")
                loc = st.text_input("Store Name")
                addr = st.text_input("Store Address")
                is_prod = st.checkbox("Is this from a Local Producer?")
                
                if st.form_submit_button("Update Logiflow"):
                    if name and loc:
                        success, msg = db.update_stock(name, loc, qty, price, exp.isoformat(), addr, is_prod)
                        if success: st.success(msg)
                        else: st.error(msg)
                    else:
                        st.error("Please fill Name and Store.")

        st.write("### Current Stock")
        st.dataframe(pd.DataFrame(db.data['inventory'])[['name', 'quantity', 'price', 'expiry_date', 'location']], use_container_width=True)

    with tab2:
        st.subheader("Incoming Messages")
        st.info("Chat messages will appear here when customers contact you via the Search Portal.")
        # Simulação de uma mensagem recebida
        st.markdown("""
        <div style="background: white; padding: 10px; border-radius: 10px; border-left: 5px solid #3498db;">
            <b>Customer:</b> "Is the Organic Milk still fresh?"
            <br><small>10:45 AM</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Reply to Customer"):
            st.text_input("Your reply:")
