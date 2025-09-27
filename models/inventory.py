from database.db import connect

def add_item(item_name, qty, threshold):
    con = connect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO inventory (item, quantity, alert_threshold) VALUES (?, ?, ?)", (item_name, qty, threshold))
    con.commit()
    con.close()
    
def get_inventory():
    """
    Fetch inventory rows with correct column names.
    """
    con = connect()
    try:
        cur = con.cursor()
        cur.execute("""
            SELECT item, quantity, alert_threshold 
            FROM inventory
        """)
        return cur.fetchall()
    finally:
        con.close()

def update_inventory(item, quantity):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE inventory SET quantity=? WHERE item=?", (quantity, item))
    con.commit()
    con.close()

def delete_inventory(item):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM inventory WHERE item=?", (item,))
    con.commit()
    con.close()
