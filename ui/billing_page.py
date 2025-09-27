import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from models.sales import record_sale

class BillingPage(tk.Frame):
    def __init__(self, parent, controller, order_items, total):
        super().__init__(parent)
        self.controller = controller
        self.order_items = order_items
        self.total = total
        
        back_btn = tk.Button(self, text="←", font=("Arial", 11),command=lambda: self.controller.show_frame("Dashboard"))
        back_btn.place(x=10, y=10)

        tk.Label(self, text="Bill Summary", font=("Arial", 16, "bold")).pack(pady=10)
        self.bill_text = tk.Text(self, width=50, height=15)
        self.bill_text.pack(side="top", fill="x", padx=20, pady=(20,10))

        button_frame = tk.Frame(self)
        button_frame.pack(side="top", pady=10)

        tk.Button(self, text="Generate Bill", command=self.generate_bill).pack(pady=5)
        tk.Button(self, text="Print Bill", command=self.print_bill).pack(pady=5)
        tk.Button(self, text="Record Sale", command=self.record_sale_in_db).pack(pady=5)
        
    def update_order(self, order_items, total):
        self.order_items = order_items
        self.total = total

        self.generate_bill(order_items, total)

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
        messagebox.showinfo("Bill Generated", "The bill has been generated.")

    def print_bill(self):
        bill_content = self.bill_text.get("1.0", tk.END)
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(bill_content)
            messagebox.showinfo("Print Bill", "Bill saved (ready for printing).")

    def record_sale_in_db(self):
        if self.order_items and self.total > 0:
            record_sale(order_id=None, amount=self.total)
            messagebox.showinfo("Sale Recorded", "This sale has been recorded in the database.")
        else:
            messagebox.showwarning("No Bill", "No bill generated to record.")
