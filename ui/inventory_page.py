import tkinter as tk
from tkinter import ttk, messagebox
from models.inventory import get_inventory, update_inventory
from database.db import connect  

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        back_btn = tk.Button(self, text="←", font=("Arial", 11),
                             command=lambda: self.controller.show_frame("Dashboard"))
        back_btn.place(x=10, y=10)

        tk.Label(self, text="Inventory Tracking & Alerts", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Item", "Qty", "Threshold", "Alert"), show="headings")         # Table to show inventory
        for col in ("Item", "Qty", "Threshold", "Alert"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        upd_frame = tk.Frame(self)            # Update Section 
        upd_frame.pack(pady=5)
        tk.Label(upd_frame, text="Item Name:").grid(row=0, column=0)
        self.item_entry = tk.Entry(upd_frame)
        self.item_entry.grid(row=0, column=1)
        tk.Label(upd_frame, text="New Qty:").grid(row=0, column=2)
        self.qty_entry = tk.Entry(upd_frame)
        self.qty_entry.grid(row=0, column=3)
        tk.Button(upd_frame, text="Update", command=self.update_stock).grid(row=0, column=4, padx=10)

        add_frame = tk.Frame(self)            # Add Item Section 
        add_frame.pack(pady=5)
        tk.Label(add_frame, text="New Item Name:").grid(row=0, column=0)
        self.new_item_entry = tk.Entry(add_frame)
        self.new_item_entry.grid(row=0, column=1)
        tk.Label(add_frame, text="Qty:").grid(row=0, column=2)
        self.new_qty_entry = tk.Entry(add_frame, width=8)
        self.new_qty_entry.grid(row=0, column=3)
        tk.Label(add_frame, text="Threshold:").grid(row=0, column=4)
        self.new_threshold_entry = tk.Entry(add_frame, width=8)
        self.new_threshold_entry.grid(row=0, column=5)
        tk.Button(add_frame, text="Add Item", command=self.add_item_func).grid(row=0, column=6, padx=10)

        del_frame = tk.Frame(self)            # Delete Item Section 
        del_frame.pack(pady=5)
        tk.Label(del_frame, text="Item to Delete:").grid(row=0, column=0)
        self.del_item_entry = tk.Entry(del_frame)
        self.del_item_entry.grid(row=0, column=1)
        tk.Button(del_frame, text="Delete Item", command=self.delete_item_func).grid(row=0, column=2, padx=10)

        tk.Button(self, text="Reload Inventory", command=self.load_inventory).pack(pady=5)            # Reload button

        self.load_inventory()
        
    def add_item_func(self):
        item = self.new_item_entry.get().strip()
        qty = self.new_qty_entry.get().strip()
        threshold = self.new_threshold_entry.get().strip()

        if not item or not qty or not threshold.isdigit():   # qty can be varchar now
            messagebox.showerror("Error", "Enter valid item name, quantity (text allowed), and numeric threshold")
            return

        con = connect()
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO inventory (item, quantity, alert_threshold) VALUES (?, ?, ?)",
                        (item, qty, int(threshold)))   # qty saved as TEXT
            con.commit()
            messagebox.showinfo("Success", f"Item '{item}' added successfully!")
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")
        finally:
            con.close()

    def delete_item_func(self):
        item = self.del_item_entry.get().strip()
        if not item:
            messagebox.showerror("Error", "Please enter an item to delete")
            return

        con = connect()
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM inventory WHERE item = ?", (item,))
            if cur.rowcount == 0:
                messagebox.showwarning("Not Found", f"No item found with name '{item}'")
            else:
                con.commit()
                messagebox.showinfo("Success", f"Item '{item}' deleted successfully!")
                self.load_inventory()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {e}")
        finally:
            con.close()

    def update_stock(self):
        item = self.item_entry.get().strip()
        qty = self.qty_entry.get().strip()
        if not item or not qty:   # allow varchar qty
            messagebox.showerror("Invalid Input", "Enter valid item name and quantity.")
            return
        update_inventory(item, qty)   # pass as TEXT
        self.load_inventory()
        messagebox.showinfo("Updated", f"Updated {item} to {qty}.")

    def update_inventory(item, quantity):
        con = connect()
        cur = con.cursor()
        cur.execute("UPDATE inventory SET quantity=? WHERE item=?", (quantity, item))  # quantity TEXT
        con.commit()
        con.close()


    def load_inventory(self):
        for item in self.tree.get_children():              # Clear table first
            self.tree.delete(item)

        inventory = get_inventory()
        low_stock = []

        for row in inventory:
            item, qty, threshold = row
            alert = "LOW" 
            try:
                if int(qty) <= threshold:     # only works if qty is numeric
                    alert = "LOW"
            except ValueError:
                pass               # skip check if qty is non-numeric (like "5kg")

            self.tree.insert("", "end", values=(item, qty, threshold, alert))

        

        
