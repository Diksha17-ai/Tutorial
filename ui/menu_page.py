import tkinter as tk
from tkinter import ttk, messagebox
from models.menu import get_menu, add_menu_item, update_menu_item, delete_menu_item

class MenuPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        back_btn = tk.Button(self, text="←", font=("Arial", 11),
                             command=lambda: self.controller.show_frame("Dashboard"))
        back_btn.place(x=10, y=10)

        tk.Label(self, text="Menu Management", font=("Arial", 16, "bold")).pack(pady=10)

        self.menu_tree = ttk.Treeview(self, columns=("ID", "Name", "Price(₹)", "Stock"), show="headings")          # Items table
        for col in ("ID", "Name", "Price(₹)", "Stock"):
            self.menu_tree.heading(col, text=col)
            self.menu_tree.column(col, anchor=tk.CENTER, width=120)
        self.menu_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.menu_tree.bind("<<TreeviewSelect>>", self.on_select)

        edit_frame = tk.Frame(self)           # Entry fields for add/edit              
        edit_frame.pack(pady=5)
        tk.Label(edit_frame, text="Name:").grid(row=0, column=0)
        self.name_e = tk.Entry(edit_frame)
        self.name_e.grid(row=0, column=1)
        tk.Label(edit_frame, text="Price:").grid(row=0, column=2)
        self.price_e = tk.Entry(edit_frame)
        self.price_e.grid(row=0, column=3)
        tk.Label(edit_frame, text="Stock:").grid(row=0, column=4)
        self.stock_e = tk.Entry(edit_frame)
        self.stock_e.grid(row=0, column=5)

        btn_frame = tk.Frame(self)            # Buttons for CRUD        
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Update Item", command=self.update_item).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Reload Menu", command=self.load_menu).grid(row=0, column=3, padx=10)

        self.selected_id = None
        self.load_menu()

    def load_menu(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        menu = get_menu()                        # [(id, name, price, stock), ...]
        for itm in menu:
            self.menu_tree.insert("", "end", values=(itm[0], itm[1], f"₹{itm[2]:.2f}", itm[3]))

        self.clear_entries()

    def on_select(self, event):
        selected = self.menu_tree.selection()
        if selected:
            values = self.menu_tree.item(selected[0])['values']
            self.selected_id = values[0]
            self.name_e.delete(0, tk.END)
            self.name_e.insert(0, values[1])
            self.price_e.delete(0, tk.END)
            self.price_e.insert(0, values[2])
            self.stock_e.delete(0, tk.END)
            self.stock_e.insert(0, values[3])

    def clear_entries(self):
        self.selected_id = None
        self.name_e.delete(0, tk.END)
        self.price_e.delete(0, tk.END)
        self.stock_e.delete(0, tk.END)

    def add_item(self):
        name = self.name_e.get().strip()
        price = self.price_e.get().strip()
        stock = self.stock_e.get().strip()
        if not name or not price.replace('.', '', 1).isdigit() or not stock.isdigit():
            messagebox.showerror("Input Error", "Enter valid name, price, and stock.")
            return
        add_menu_item(name, float(price), int(stock))
        self.load_menu()
        messagebox.showinfo("Added", f"Menu item '{name}' added.")

    def update_item(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select an item to update.")
            return
        name = self.name_e.get().strip()
        price = self.price_e.get().strip()
        stock = self.stock_e.get().strip()
        if not name or not price.replace('.', '', 1).isdigit() or not stock.isdigit():
            messagebox.showerror("Input Error", "Enter valid name, price, and stock.")
            return
        update_menu_item(self.selected_id, name, float(price), int(stock))
        self.load_menu()
        messagebox.showinfo("Updated", f"Menu item '{name}' updated.")

    def delete_item(self):
        if not self.selected_id:
            messagebox.showwarning("No Selection", "Select an item to delete.")
            return
        delete_menu_item(self.selected_id)
        self.load_menu()
        messagebox.showinfo("Deleted", "Menu item deleted.")

