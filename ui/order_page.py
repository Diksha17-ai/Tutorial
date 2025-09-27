import tkinter as tk
from tkinter import ttk, messagebox
from models.order import create_order
from models.menu import get_menu  # Needed to fetch menu items
from ui.billing_page import BillingPage

class OrderPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.order_items = []  
        self.total_var = tk.StringVar(value="0.00")

        back_btn = tk.Button(self, text="←", font=("Arial", 11), command=lambda: self.controller.show_frame("Dashboard"))
        back_btn.place(x=10, y=10)

        tk.Label(self, text="Order Entry & Customization", font=("Arial", 16, "bold")).pack(pady=10)

        self.menu_tree = ttk.Treeview(self, columns=("id", "name", "price", "stock"), show="headings", height=6) #Available items table (from menu)
        for col in ("ID", "Name", "Price", "Stock"), (60, 200, 100, 100):
            self.menu_tree.heading("id", text="ID")                          # Set headings
            self.menu_tree.heading("name", text="Name")
            self.menu_tree.heading("price", text="Price")
            self.menu_tree.heading("stock", text="Stock")
           
            self.menu_tree.column("id", anchor=tk.CENTER, width=60)          # Set column alignment & widths
            self.menu_tree.column("name", anchor=tk.CENTER, width=200)
            self.menu_tree.column("price", anchor=tk.CENTER, width=100)
            self.menu_tree.column("stock", anchor=tk.CENTER, width=100)

            self.menu_tree.pack(fill="x", padx=8, pady=8)
        
        tk.Button(self, text="Reload Menu", command=self.load_menu).pack(pady=4)
        self.menu_tree.bind("<<TreeviewSelect>>", self.on_menu_select)

        cart_frame = tk.Frame(self)            # Quantity selection and add-to-order controls
        cart_frame.pack(pady=5)
        tk.Label(cart_frame, text="Selected Item:").grid(row=0, column=0)
        self.sel_name = tk.Entry(cart_frame, width=15, state='readonly')
        self.sel_name.grid(row=0, column=1)
        tk.Label(cart_frame, text="Quantity:").grid(row=0, column=2)
        self.sel_qty = tk.Entry(cart_frame, width=5)
        self.sel_qty.grid(row=0, column=3)
        tk.Button(cart_frame, text="Add to Order", command=self.add_to_order).grid(row=0, column=4, padx=10)

        tk.Label(self, text="Current Order", font=("Arial", 14)).pack(pady=7)               # Order summary table
        table_frame = tk.Frame(self)
        table_frame.pack(fill="x", padx=10)

        self.order_tree = ttk.Treeview(table_frame, columns=("name", "qty", "unit_price", "total"), show="headings", height=6)       # Order table
        for col in zip(("Name", "Qty", "Unit Price", "Total"), (200, 80, 100, 100)):
            self.order_tree.heading("name", text="Name")            # Headings (visible text)
            self.order_tree.heading("qty", text="Qty")
            self.order_tree.heading("unit_price", text="Unit Price")
            self.order_tree.heading("total", text="Total")

            self.order_tree.column("name", anchor=tk.CENTER, width=200)             # Column widths
            self.order_tree.column("qty", anchor=tk.CENTER, width=80)
            self.order_tree.column("unit_price", anchor=tk.CENTER, width=100)
            self.order_tree.column("total", anchor=tk.CENTER, width=100)

            self.order_tree.pack(fill="x")

        bottom_frame = tk.Frame(self)                  #  Bottom Frame (Total + Submit + Reset) 
        bottom_frame.pack(pady=8)

        tk.Label(bottom_frame, text="Order Total (₹):", font=("Arial", 12)).grid(row=0, column=0, sticky="w")         # Total label + value
        tk.Label(bottom_frame, textvariable=self.total_var, font=("Arial", 13, "bold")).grid(row=0, column=1, padx=10)

        submit_btn = tk.Button(bottom_frame, text="Submit Order", command=self.submit_order)      # Buttons (side by side under total)
        submit_btn.grid(row=1, column=0, pady=8, padx=5, sticky="ew")

        reset_btn = tk.Button(bottom_frame, text="Reset Order", command=self.reset_order)
        reset_btn.grid(row=1, column=1, pady=8, padx=5, sticky="ew")

        self.load_menu()

    def load_menu(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)
        menu = get_menu()
        for itm in menu:
            self.menu_tree.insert("", "end", values=itm)
            self.sel_name.config(state='normal')
            self.sel_name.delete(0, tk.END)
            self.sel_name.config(state='readonly')
            self.sel_qty.delete(0, tk.END)

    def on_menu_select(self, event):
        selected = self.menu_tree.selection()
        if selected:
            values = self.menu_tree.item(selected[0])['values']
            self.sel_name.config(state='normal')
            self.sel_name.delete(0, tk.END)
            self.sel_name.insert(0, values[1])
            self.sel_name.config(state='readonly')

    def add_to_order(self):
        item_name = self.sel_name.get().strip()
        qty_str = self.sel_qty.get().strip()

        if not item_name or not qty_str.isdigit():
            messagebox.showerror("Input Error", "Select item and enter a valid quantity.")
            return

        qty = int(qty_str)
        menu = get_menu()
        selected_item = next((i for i in menu if i[1] == item_name), None)

        if not selected_item:
            messagebox.showerror("Selection Error", "Selected item not found in menu.")
            return

        unit_price = selected_item[2]
        total = qty * unit_price

        if qty > selected_item[3]:
            messagebox.showwarning("Stock Error", "Requested quantity exceeds stock!")
            return

        self.order_items.append({"name": item_name, "qty": qty, "price": unit_price, "total": total})
        self.order_tree.insert("", "end", values=(item_name, qty, f"₹{unit_price:.2f}", f"₹{total:.2f}"))

        self.update_total()
        self.sel_name.config(state='normal')
        self.sel_name.delete(0, tk.END)
        self.sel_name.config(state='readonly')
        self.sel_qty.delete(0, tk.END)


    def update_total(self):
        total = sum(item["total"] for item in self.order_items)
        self.total_var.set(f"{total:.2f}")

    def submit_order(self):
        if not self.order_items:
            messagebox.showwarning("No Items", "No items in current order.")
            return
        order_items_str = ', '.join([f"{itm['name']} x{itm['qty']}" for itm in self.order_items])
        total = float(self.total_var.get())

        order_id = create_order(order_items_str, total)
        messagebox.showinfo("Order Submitted", f"Order submitted!\nTotal: ₹{self.total_var.get()}")
        order_copy = self.order_items.copy()

        billing_page = BillingPage(self.master, self.controller, self.order_items.copy(), total=total)
        billing_page.grid(row=0, column=0, sticky="nsew")
        self.controller.frames["BillingPage"] = billing_page
        self.controller.show_frame("BillingPage")
    
    def reset_order(self):
        self.order_items.clear()
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        self.total_var.set("0.00")
        messagebox.showinfo("Order Reset", "The current order has been cleared.")

    def generate_bill(self):
        self.bill_text.delete("1.0", tk.END)
        self.bill_text.insert(tk.END, "Cafe XYZ\n")
        self.bill_text.insert(tk.END, "-"*50 + "\n")
        self.bill_text.insert(tk.END, "{:<25}{:<10}{:<10}\n".format("Item", "Qty", "Price  (₹)"))
        self.bill_text.insert(tk.END, "-"*50 + "\n")
        for item in self.order_items:
            name, qty, price = item['name'], item['qty'], item['price']
            self.bill_text.insert(tk.END, "{:<25}{:<10}₹{:<10.2f}\n".format(name, qty, price))
        self.bill_text.insert(tk.END, "-"*50 + "\n")
        self.bill_text.insert(tk.END, f"{'Total':<25}{'':<10}₹{self.total:.2f}\n")
        self.bill_text.insert(tk.END, "-"*50 + "\n")
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Bill Generated", "The bill has been generated.")

        self.total = total                  # Optionally store total as self.total if generate_bill uses it

        self.generate_bill()                #  GENERATE BILL
        self.order_items = []               # Reset order
        self.refresh_order_table()
        self.load_menu()

    