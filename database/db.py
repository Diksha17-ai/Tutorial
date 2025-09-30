import sqlite3

def connect():
    return sqlite3.connect("cafe.db")  

def init_db():
    con = connect()
    cur = con.cursor()

    conn = sqlite3.connect("cafe.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT,
        amount REAL
    )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT UNIQUE NOT NULL,
            quantity TEXT NOT NULL,
            alert_threshold INTEGER NOT NULL DEFAULT 0
        )
    """)      # Create inventory table                         

    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)       # Create menu table 

    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)", ("Espresso", 120.0, 10))      # Insert sample rows
    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)", ("Latte", 150.0, 8))
    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)", ("Muffin", 80.0, 5))

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_items TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)       # Create Orders table


    con.commit()
    con.close()

    print("Sample menu inserted.")
