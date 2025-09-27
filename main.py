from database.db import init_db
import tkinter as tk
from ui.dashboard import Dashboard
from ui.menu_page import MenuPage
from ui.order_page import OrderPage
from ui.billing_page import BillingPage
from ui.inventory_page import InventoryPage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cafe Management System")
        self.geometry("600x500")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Dashboard, MenuPage, OrderPage, InventoryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        billing_page = BillingPage(parent=container, controller=self, order_items=[], total=0.0)
        billing_page.grid(row=0, column=0, sticky="nsew")
        self.frames["BillingPage"] = billing_page

        self.show_frame("Dashboard")                  # Show home page at start

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    init_db
    app = MainApp()
    app.mainloop()
