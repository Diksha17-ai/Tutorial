from database.db import connect

def create_order(order_items, total):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO orders (order_items, total) VALUES (?, ?)", (order_items, total))
    con.commit()
    return cur.lastrowid
