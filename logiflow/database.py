import sqlite3
import datetime
import random
import pandas as pd

class LogiflowDB:
    def __init__(self, db_name="logiflow_final.db"):
        self.db_name = db_name
        self._setup_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _setup_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("DROP TABLE IF EXISTS inventory")
        
        cursor.execute('''CREATE TABLE products (
                            product_id INTEGER PRIMARY KEY,
                            name TEXT,
                            is_perishable BOOLEAN,
                            is_producer BOOLEAN)''')

        cursor.execute('''CREATE TABLE inventory (
                            item_id INTEGER PRIMARY KEY,
                            product_id INTEGER,
                            quantity INTEGER,
                            location TEXT,
                            expiry_date DATE,
                            price REAL,
                            last_updated TIMESTAMP,
                            discount_pct REAL,
                            address TEXT,
                            FOREIGN KEY(product_id) REFERENCES products(product_id))''')

        products = [
            (1, "Organic Milk", 1, 0),
            (2, "Fresh Avocado", 1, 1),
            (3, "Greek Yogurt", 1, 0),
            (4, "Sourdough Bread", 1, 1),
            (5, "Canned Beans", 0, 0)
        ]
        cursor.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
        conn.commit()
        conn.close()
        self.seed_initial_inventory()

    def seed_initial_inventory(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        today = datetime.date.today()
        inventory = [
            (1, 1, 20, "Main St Shop", (today + datetime.timedelta(days=10)).isoformat(), 4.50, today.isoformat(), 0.0, "123 Market Ave"),
            (2, 2, 15, "Green Corner", (today + datetime.timedelta(days=1)).isoformat(), 2.0, today.isoformat(), 0.0, "45 Farm Road")
        ]
        cursor.executemany("INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?)", inventory)
        conn.commit()
        conn.close()
