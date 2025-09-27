# seed_data.py
from database.db import connect

def seed_data():
    con = connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT UNIQUE NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            alert_threshold INTEGER NOT NULL DEFAULT 0
        )
    """)         # Create inventory table if missing

    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)         # Create menu table if missing

    cur.execute("INSERT OR IGNORE INTO inventory (item, quantity, alert_threshold) VALUES (?, ?, ?)",
                ("Espresso", 10, 5))
    cur.execute("INSERT OR IGNORE INTO inventory (item, quantity, alert_threshold) VALUES (?, ?, ?)",
                ("Latte", 8, 3))
    cur.execute("INSERT OR IGNORE INTO inventory (item, quantity, alert_threshold) VALUES (?, ?, ?)",
                ("Muffin", 2, 2))                                                                            # Seed Inventory
   
    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)",
                ("Espresso", 120.0, 10))
    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)",
                ("Latte", 150.0, 8))
    cur.execute("INSERT OR IGNORE INTO menu (name, price, stock) VALUES (?, ?, ?)",
                ("Muffin", 80.0, 5))                                                        # Seed Menu 

    con.commit()
    con.close()
    print(" Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
