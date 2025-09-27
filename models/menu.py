from database.db import connect

def get_menu():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM menu")
    return cur.fetchall()

def add_menu_item(name, price, stock):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO menu (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    con.commit()

def update_menu_item(item_id, name, price, stock):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE menu SET name=?, price=?, stock=? WHERE id=?", (name, price, stock, item_id))
    con.commit()

def delete_menu_item(item_id):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM menu WHERE id=?", (item_id,))
    con.commit()
