import tkinter as tk

class Dashboard(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self):
        welcome = tk.Label(self, text="Welcome to Cafe Management System", font=("Arial", 20, "bold"))             # Welcome label
        welcome.pack(pady=30)

        nav_frame = tk.Frame(self)       # Navigation buttons frame
        nav_frame.pack(pady=40)

        btn_menu = tk.Button(nav_frame, text="Menu Management", width=20, command=lambda: self.controller.show_frame("MenuPage"))
        btn_order = tk.Button(nav_frame, text="Order Entry", width=20,command=lambda: self.controller.show_frame("OrderPage"))
        btn_billing = tk.Button(nav_frame, text="Billing", width=20,command=lambda: self.controller.show_frame("BillingPage"))
        btn_inventory = tk.Button(nav_frame, text="Inventory", width=20,command=lambda: self.controller.show_frame("InventoryPage"))

        btn_menu.grid(row=0, column=0, padx=20, pady=10)
        btn_order.grid(row=0, column=1, padx=20, pady=10)
        btn_billing.grid(row=1, column=0, padx=20, pady=10)
        btn_inventory.grid(row=1, column=1, padx=20, pady=10)

    def show_page(self, page_name):
        tk.messagebox.showinfo("Navigation", f"Switch to the '{page_name}' page.")

if __name__ == "__main__":
    root = tk.Tk()                         # Dashboard intgration
    root.title("Cafe Management System")
    root.geometry("600x400")
    Dashboard(root)
    root.mainloop()
    main()


