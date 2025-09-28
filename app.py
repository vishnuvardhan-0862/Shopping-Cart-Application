import tkinter as tk
from tkinter import ttk, messagebox
import sys
from io import StringIO

# Add the project root to the Python path to allow imports from the 'backend' folder
sys.path.append('.')

# Import backend logic functions and data

from products.products import products
from cart.view_cart import view_cart
from cart.add_to_cart import add_to_cart
from cart.update_cart import update_cart
from cart.remove_from_cart import remove_from_cart
from cart.checkout import checkout

# Global variable for the cart 
cart = []

# UI Styling Constants 
BG_COLOR = "#2c3e50"
FG_COLOR = "#ecf0f1"
BTN_BG_COLOR = "#3498db"
BTN_FG_COLOR = "#ffffff"
SUCCESS_COLOR = "#2ecc71"
ERROR_COLOR = "#e74c3c"
FONT_NORMAL = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 12, "bold")
FONT_TITLE = ("Helvetica", 16, "bold")


class ShoppingApp:
    """The main window for the shopping application."""
    def __init__(self, root):
        self.root = root
        self._setup_main_window()
        self._create_widgets()
        self.populate_products_tree()

    def _setup_main_window(self):
        """Configures the main window properties."""
        self.root.title("Retail Therapy")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG_COLOR)

    def _create_widgets(self):
        """Creates and arranges all the UI elements in the main window."""
        main_frame = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Products Frame (Left) 
        products_frame = tk.Frame(main_frame, bg=BG_COLOR)
        products_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tk.Label(products_frame, text="Available Products", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)
        
        self.products_tree = self._create_treeview(products_frame, ["ID", "Brand", "Name", "Price (₹)"])
        self.products_tree.pack(fill=tk.BOTH, expand=True)
        self._style_treeview(self.products_tree)

        # Controls Frame (Middle)
        controls_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10)
        controls_frame.grid(row=0, column=1, sticky="ns", pady=20)

        tk.Label(controls_frame, text="Product ID:", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        self.product_id_entry = tk.Entry(controls_frame, font=FONT_NORMAL, width=10, justify='center')
        self.product_id_entry.pack(pady=5)

        tk.Label(controls_frame, text="Quantity:", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        self.quantity_entry = tk.Entry(controls_frame, font=FONT_NORMAL, width=10, justify='center')
        self.quantity_entry.pack(pady=5)

        self._create_button(controls_frame, "Add to Cart", self.add_item_to_cart, SUCCESS_COLOR)
        self._create_button(controls_frame, "Update Cart", self.update_item_in_cart)
        self._create_button(controls_frame, "Remove from Cart", self.remove_item_from_cart, ERROR_COLOR)
        self._create_button(controls_frame, "Checkout", self.checkout)
        self._create_button(controls_frame, "Exit", self.root.quit, "#7f8c8d")
        
        # Cart Frame (Right) 
        cart_frame = tk.Frame(main_frame, bg=BG_COLOR)
        cart_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        tk.Label(cart_frame, text="Your Cart", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        self.cart_tree = self._create_treeview(cart_frame, ["ID", "Name", "Qty", "Price", "Subtotal"])
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        self._style_treeview(self.cart_tree)
        
        self.total_label = tk.Label(cart_frame, text="Grand Total: ₹0.00", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR)
        self.total_label.pack(pady=10, anchor="e")

        # Configure grid weights for responsive resizing
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=3)
        main_frame.grid_rowconfigure(0, weight=1)

    def _create_treeview(self, parent, columns):
        """Helper function to create a styled Treeview widget."""
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        return tree

    def _style_treeview(self, tree):
        """Applies custom styling to a Treeview widget."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#34495e", foreground=FG_COLOR, rowheight=25, fieldbackground="#34495e", font=FONT_NORMAL)
        style.map('Treeview', background=[('selected', BTN_BG_COLOR)])
        style.configure("Treeview.Heading", font=FONT_BOLD, background="#2c3e50", foreground=FG_COLOR)

    def _create_button(self, parent, text, command, bg_color=BTN_BG_COLOR):
        """Helper function to create a styled Button."""
        button = tk.Button(parent, text=text, command=command, font=FONT_BOLD, bg=bg_color, fg=BTN_FG_COLOR, relief=tk.FLAT, padx=10, pady=5, width=15)
        button.pack(pady=10)

    def populate_products_tree(self):
        """Fills the products table with data from the products list."""
        for product in products:
            self.products_tree.insert('', tk.END, values=(product["id"], product["brand"], product["name"], f'{product["price"]:.2f}'))

    def refresh_cart_display(self):
        """Clears and re-populates the cart view with the latest data."""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        grand_total = 0
        for item in cart:
            subtotal = item['price'] * item['quantity']
            grand_total += subtotal
            self.cart_tree.insert('', tk.END, values=(item['id'], f"{item['brand']} {item['name']}", item['quantity'], f"₹{item['price']:.2f}", f"₹{subtotal:.2f}"))
        
        self.total_label.config(text=f"Grand Total: ₹{grand_total:.2f}")

    def _execute_backend_action(self, action_func, *args):
        
        original_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        action_func(*args)
        
        sys.stdout = original_stdout
        return captured_output.getvalue().strip()

    def add_item_to_cart(self):
        try:
            pid = int(self.product_id_entry.get())
            qty = int(self.quantity_entry.get())
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0.")
                return

            message = self._execute_backend_action(add_to_cart, products, cart, pid, qty)
            
            if "added" in message or "Updated" in message:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showwarning("Warning", message)

            self.refresh_cart_display()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for Product ID and Quantity.")

    def update_item_in_cart(self):
        try:
            pid = int(self.product_id_entry.get())
            qty = int(self.quantity_entry.get())
            
            message = self._execute_backend_action(update_cart, cart, pid, qty)
            
            if "updated" in message:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
                
            self.refresh_cart_display()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for Product ID and Quantity.")

    def remove_item_from_cart(self):
        try:
            pid_str = self.product_id_entry.get()
            if not pid_str:
                selected_item = self.cart_tree.focus()
                if not selected_item:
                    messagebox.showerror("Error", "Enter a Product ID or select an item from the cart to remove.")
                    return
                pid = self.cart_tree.item(selected_item)['values'][0]
            else:
                pid = int(pid_str)

            message = self._execute_backend_action(remove_from_cart, cart, pid)

            if "removed" in message:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

            self.refresh_cart_display()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid Product ID.")
            
    def checkout(self):
        if not cart:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Nothing to checkout.")
            return

        bill_details = "===== Final Bill =====\n"
        total = 0
        for item in cart:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            bill_details += f"{item['brand']} {item['name']} - ₹{item['price']:.2f} x {item['quantity']} = ₹{subtotal:.2f}\n"
        
        bill_details += "-" * 30 + "\n"
        bill_details += f"Grand Total: ₹{total:.2f}\n"
        bill_details += "=" * 30

        if messagebox.askokcancel("Confirm Checkout", bill_details + "\n\nProceed with payment?"):
            cart.clear()
            self.refresh_cart_display()
            messagebox.showinfo("Thank You!", "Thank you for shopping with us!")

    def clear_entries(self):
        self.product_id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


class LoginWindow:
    """The initial login window for user authentication."""
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_COLOR)

        self.main_frame = tk.Frame(self.root, bg=BG_COLOR, pady=40)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text="User Login", font=FONT_TITLE, bg=BG_COLOR, fg=FG_COLOR).pack(pady=(0, 20))

        tk.Label(self.main_frame, text="Username", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack()
        self.username_entry = tk.Entry(self.main_frame, font=FONT_NORMAL, width=20, justify='center')
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "VISHNU")

        tk.Label(self.main_frame, text="Password", font=FONT_BOLD, bg=BG_COLOR, fg=FG_COLOR).pack()
        self.password_entry = tk.Entry(self.main_frame, font=FONT_NORMAL, show="*", width=20, justify='center')
        self.password_entry.pack(pady=5)
        self.password_entry.insert(0, "mr.dreamer0862")

        self._create_button(self.main_frame, "Login", self.login, SUCCESS_COLOR)

    def _create_button(self, parent, text, command, bg_color=BTN_BG_COLOR):
        button = tk.Button(parent, text=text, command=command, font=FONT_BOLD, bg=bg_color, fg=BTN_FG_COLOR, relief=tk.FLAT, padx=10, pady=5, width=15)
        button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "VISHNU" and password == "mr.dreamer0862":
            self.root.destroy()
            main_app_window = tk.Tk()
            ShoppingApp(main_app_window)
            main_app_window.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
