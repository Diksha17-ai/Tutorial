from database.db import connect
import sqlite3

def record_sale(order_id, amount):
    conn = sqlite3.connect("cafe.db") 
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        amount REAL
    )
    """)        # Ensure the 'sales' table exists
    
    cur.execute("INSERT INTO sales (order_id, amount) VALUES (?, ?)", (order_id, amount))           # Insert the sale record
    
    conn.commit()          # Commit changes and close connection
    conn.close()

def get_total_sales():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT SUM(amount) FROM sales")
    return cur.fetchone()[0]
