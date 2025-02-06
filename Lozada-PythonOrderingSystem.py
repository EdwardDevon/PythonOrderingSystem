import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime

class Product:
    def __init__(self, master, name, price, image_path, add_to_cart_callback, row, column):
        self.master = master
        self.name = name
        self.price = price
        self.image_path = image_path
        self.quantity = tk.IntVar(value=1)
        self.add_to_cart_callback = add_to_cart_callback
        self.row = row
        self.column = column

        self.create_widgets()

    def create_widgets(self):
        # Load and display the product image
        image = Image.open(self.image_path).resize((150, 130))
        photo = ImageTk.PhotoImage(image)

        # Create frame for product
        self.frame = tk.Frame(self.master, bd=2, relief="solid")
        self.frame.grid(row=self.row, column=self.column, padx=5, pady=5)

        # Create and place image label
        self.image_label = tk.Label(self.frame, image=photo)
        self.image_label.image = photo  # Keep a reference to avoid garbage collection
        self.image_label.pack()

        # Create and place name label
        self.name_label = tk.Label(self.frame, text=self.name, fg="#38B6FF", font=("Helvetica", 8, "bold"))
        self.name_label.pack()

        # Create and place price label
        self.price_label = tk.Label(self.frame, text=f"${self.price:.2f}",fg="#40A578", font=("Helvetica", 7, "bold"))
        self.price_label.pack(pady=2)

        # Create and place Spinbox for quantity
        self.spinbox = tk.Spinbox(self.frame, from_=0, to=100, textvariable=self.quantity, width=5)
        self.spinbox.pack(fill="x", padx=10, pady=5)

        # Create and place Add button
        self.add_button = tk.Button(self.frame, text="ADD", command=self.add_to_cart,width=7, bg="tomato", fg="white", font=("Helvetica",10, "bold"))
        self.add_button.pack(pady=5)

    def add_to_cart(self):
        quantity = self.quantity.get()
        if quantity > 0:
            total_price = self.price * quantity
            self.add_to_cart_callback(self.name, quantity, total_price)
        else:
            messagebox.showwarning("Invalid Quantity", "Please select a quantity greater than 0.")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordering System")
        self.make_fullscreen()

        self.cart = {}
        self.total_amount = 0.0
        self.discount_percentage = 0.0
        self.products_list = []  # List to hold Product instances

        self.create_left_section()
        self.create_product_section()
        self.create_cart_section()
        self.create_receipt_section()


    def make_fullscreen(self):
        self.root.state('zoomed')

    def create_left_section(self):
        left_frame = tk.Frame(self.root, width=200, relief="solid", bd=1, padx=10, bg="#686D76")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # User image
        user_image = Image.open("images/user_icon.png").resize((150, 150))
        user_photo = ImageTk.PhotoImage(user_image)
        user_image_label = tk.Label(left_frame, image=user_photo)
        user_image_label.image = user_photo
        user_image_label.pack(pady=10)

        # User name
        user_name_label = tk.Label(left_frame,bg="#686D76", fg="white", text="CASHIER 1", font=("Helvetica", 16))
        user_name_label.pack(pady=10)

        # Current time and date
        self.time_label = tk.Label(left_frame, bg="#686D76", fg="white", text="", font=("Helvetica", 12))
        self.time_label.pack(pady=10)
        self.update_time()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update time every second

    def create_product_section(self):
        products_frame = tk.Frame(self.root, width=700, relief="solid", bd=0)
        products_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=0)

        self.products = [
            {"name": "iPhone11 Pro Max Gold", "price": 10.00, "image": "images/product1.png"} ,
            {"name": "iPhone11 Pro Max Black", "price": 20.00, "image": "images/product2.png"},
            {"name": "iPhone12 Pro Max 512GB", "price": 15.00, "image": "images/product3.png"},
            {"name": "AirPods 3rd Gen", "price": 12.00, "image": "images/product4.png"},
            {"name": "Apple Watch SE", "price": 25.00, "image": "images/product5.png"},
            {"name": "Apple AirPods Max - Silver", "price": 30.00, "image": "images/product6.png"},
            {"name": "Apple 20W Fast Charger", "price": 18.00, "image": "images/product7.png"},
            {"name": "Apple iPad (9th Generation) Wi-Fi", "price": 22.00, "image": "images/product8.png"},
            {"name": "Apple MacBook Pro 13 (2022)", "price": 16.00, "image": "images/product9.png"}
        ]

        row, column = 0, 0
        for index, product in enumerate(self.products):
            Product(products_frame, product["name"], product["price"], product["image"], self.add_to_cart, row, column)
            column += 1
            if column > 2:
                column = 0
                row += 1

        for i in range(3):
            products_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            products_frame.grid_rowconfigure(i, weight=1)

    def create_cart_section(self):
        cart_frame = tk.Frame(self.root, width=300, relief="solid", bd=0, bg="#FEFFD2")
        cart_frame.pack(side=tk.LEFT, padx=5, pady=10, anchor="n", fill="y")

        self.cart_label = tk.Label(cart_frame, text="Current Order Status", bg="#FEFFD2",  fg="#40A578", font=("Helvetica", 11, "bold"))
        self.cart_label.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        self.clear_button = tk.Button(cart_frame, text="CLEAR", command=self.clear_cart, width=15, height=1, bg="Tomato", fg="White",font=("Helvetica", 11, "bold"))
        self.clear_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        self.cart_tree = ttk.Treeview(cart_frame, columns=("Name", "Quantity", "Total Price"), show="headings", height=3)
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Quantity", text="Quantity")
        self.cart_tree.heading("Total Price", text="Total Price")
        self.cart_tree.column("Name", width=200)
        self.cart_tree.column("Quantity", width=100)
        self.cart_tree.column("Total Price", width=150)
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        buttons_frame = tk.Frame(cart_frame, width=300, bg="#FEFFD2")
        buttons_frame.pack(side=tk.TOP,fill="x", padx=1, pady=10)

        self.discount_button = tk.Button(buttons_frame,text="DISCOUNT", command=self.prompt_discount, width=15, height=1, bg="#FFBF00", fg="WHITE", font=("Helvetica", 11, "bold"))
        self.discount_button.pack(side=tk.LEFT,padx=10,anchor=tk.NW, pady=10)

        self.pay_button = tk.Button(buttons_frame,text="PAY", command=self.prompt_payment, width=15, height=1, bg="#A1DD70", fg="white", font=("Helvetica", 11, "bold"))
        self.pay_button.pack(side=tk.RIGHT,padx=10,anchor=tk.NE, pady=10)

        self.payment_label = tk.Label(cart_frame, text="Amount Paid: $0.00", fg="#40A578", bg="#FEFFD2", font=("Helvetica", 11, "bold"))
        self.payment_label.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=5)

        self.change_label = tk.Label(cart_frame, text="Change: $0.00", fg="#40A578", bg="#FEFFD2", font=("Helvetica", 11, "bold"))
        self.change_label.pack(side=tk.TOP, padx=10, pady=5,  anchor=tk.NE)

        self.discount_label = tk.Label(cart_frame, text="Discount Percentage: 0.0%", bg="#FEFFD2",  fg="#40A578", font=("Helvetica", 11, "bold"))
        self.discount_label.pack(side=tk.TOP,padx=10,anchor=tk.NW)

        self.discounted_price_label = tk.Label(cart_frame, text="Total Discount: $0.00", bg="#FEFFD2",  fg="#40A578", font=("Helvetica", 11, "bold"))
        self.discounted_price_label.pack(side=tk.TOP,padx=10,anchor=tk.NW)

        self.total_label = tk.Label(cart_frame, text="Total: $0.00", fg="#40A578", bg="#FEFFD2", font=("Helvetica", 11, "bold"))
        self.total_label.pack(side=tk.LEFT, padx=10, pady=5)


    def create_receipt_section(self):
        receipt_frame = tk.Frame(self.root, width=300, relief="solid", bd=2)
        receipt_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.receipt_text = tk.Text(receipt_frame, state=tk.DISABLED)
        self.receipt_text.pack(fill=tk.BOTH, expand=True)

        self.print_button = tk.Button(receipt_frame, text="PRINT RECEIPT", command=self.print_receipt, width=20, height=2, bg="#7E8EF1", fg="white", font=("Helvetica", 11, "bold"))
        self.print_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def add_to_cart(self, name, quantity, total_price):
        if name in self.cart:
            self.cart[name]["quantity"] += quantity
            self.cart[name]["total_price"] += total_price
        else:
            self.cart[name] = {"quantity": quantity, "total_price": total_price}

        self.update_cart()
        self.update_receipt()

    def update_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.total_amount = 0.0
        for name, details in self.cart.items():
            self.cart_tree.insert("", tk.END, values=(name, details["quantity"], f"${details['total_price']:.2f}"))
            self.total_amount += details["total_price"]

        self.update_total_label()

    def clear_cart(self):
        self.cart.clear()
        self.discount_percentage = 0.0
        self.update_cart()
        self.update_receipt()
        self.discount_label.config(text="Discount Percentage: 0.0%")
        self.discounted_price_label.config(text="Discounted Price: $0.00")
        self.total_label.config(text="Total: $0.00")
        self.change_label.config(text="Change: $0.00")
        self.payment_label.config(text="Amount Paid: $0.00")


    def prompt_discount(self):
        discount_percentage = simpledialog.askfloat("Discount", "Enter discount percentage:", minvalue=0, maxvalue=100)
        if discount_percentage is not None:
            self.discount_percentage = discount_percentage
            self.apply_discount()

    def apply_discount(self):
        discount_amount = (self.discount_percentage / 100) * self.total_amount
        discounted_price = self.total_amount - discount_amount
        self.discount_label.config(text=f"Discount Percentage: {self.discount_percentage}%")
        self.discounted_price_label.config(text=f"Total Discount: ${discount_amount:.2f}")
        self.update_total_label(discounted_price)
        self.update_receipt()

    def prompt_payment(self):
        amount_paid = simpledialog.askfloat("Payment", "Enter the amount paid:", minvalue=0)
        if amount_paid is not None:
            self.payment_label.config(text=f"Amount Paid: ${amount_paid:.2f}")
            self.calculate_change(amount_paid)

    def calculate_change(self, amount_paid=None):
        if amount_paid is None:
            try:
                amount_paid = float(self.payment_entry.get())
                self.payment_label.config(text=f"Amount Paid: ${amount_paid:.2f}")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
                return

        discount_amount = (self.discount_percentage / 100) * self.total_amount
        discounted_price = self.total_amount - discount_amount
        change = amount_paid - discounted_price
        self.change_label.config(text=f"Change: ${change:.2f}")

    def update_total_label(self, discounted_price=None):
        if discounted_price is None:
            discounted_price = self.total_amount
        self.total_label.config(text=f"Total: ${discounted_price:.2f}")


    def update_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update time every second

    def update_receipt(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)  # Update time every second
        self.receipt_text.config(state=tk.NORMAL)
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, "Receipt\t\t")
        self.receipt_text.insert(tk.END, current_time, "\n")
        self.receipt_text.insert(tk.END, "-----------------------------------\n\n")
        for name, details in self.cart.items():
            self.receipt_text.insert(tk.END, f"{name} x{details['quantity']} - ${details['total_price']:.2f}\n\n")
        discount_amount = (self.discount_percentage / 100) * self.total_amount
        discounted_price = self.total_amount - discount_amount
        self.receipt_text.insert(tk.END, "-----------------------------------\n\n")
        self.receipt_text.insert(tk.END, f"Total (before discount): ${self.total_amount:.2f}\n\n")
        self.receipt_text.insert(tk.END, f"Discount ({self.discount_percentage}%): -${discount_amount:.2f}\n\n")
        self.receipt_text.insert(tk.END, f"Total (after discount): ${discounted_price:.2f}\n\n")
        self.receipt_text.config(state=tk.DISABLED)


    def print_receipt(self):
        print_content = self.receipt_text.get("1.0", tk.END)
        print_window = tk.Toplevel(self.root)
        print_window.title("Receipt")
        print_text = tk.Text(print_window)
        print_text.pack(fill=tk.BOTH, expand=True)
        print_text.insert(tk.END, print_content)



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
