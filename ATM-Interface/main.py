# Python Code with MySQL Database Integration

import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ATM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("300x400")
        
        # Establish Database Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="Mayank",
            password="Rcf@634e",  
            database="atm_db"
        )
        self.cursor = self.db.cursor()

        self.current_pin = None
        self.create_login_screen()
    
    def create_login_screen(self):
        """Create the login screen."""
        self.clear_window()
        
        tk.Label(self.root, text="Enter PIN:", font=("Arial", 14)).pack(pady=10)
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.pin_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.authenticate).pack(pady=10)

    def authenticate(self):
        """Check user PIN for authentication from MySQL database."""
        pin = self.pin_entry.get()
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (pin,))
        result = self.cursor.fetchone()

        if result:
            self.current_pin = pin
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Incorrect PIN. Try again.")

    def create_menu_screen(self):
        """Display the ATM menu options."""
        self.clear_window()
        
        tk.Label(self.root, text="ATM Menu", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(self.root, text="Check Balance", font=("Arial", 14), command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.create_login_screen).pack(pady=10)

    def check_balance(self):
        """Fetch and show balance from database."""
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
        balance = self.cursor.fetchone()[0]
        messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")

    def deposit_screen(self):
        """Create deposit screen."""
        self.clear_window()
        
        tk.Label(self.root, text="Enter amount to deposit:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.deposit).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_menu_screen).pack(pady=5)

    def deposit(self):
        """Deposit money and update balance in the database."""
        amount = self.amount_entry.get()
        if amount.isdigit() and float(amount) > 0:
            amount = float(amount)
            self.cursor.execute("UPDATE users SET balance = balance + %s WHERE pin = %s", (amount, self.current_pin))
            self.db.commit()
            messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!")
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Invalid deposit amount.")

    def withdraw_screen(self):
        """Create withdrawal screen."""
        self.clear_window()
        
        tk.Label(self.root, text="Enter amount to withdraw:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.withdraw).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_menu_screen).pack(pady=5)

    def withdraw(self):
        """Withdraw money and update balance in the database."""
        amount = self.amount_entry.get()
        if amount.isdigit() and float(amount) > 0:
            amount = float(amount)
            
            # Fetch current balance
            self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
            balance = self.cursor.fetchone()[0]
            
            if amount <= balance:
                self.cursor.execute("UPDATE users SET balance = balance - %s WHERE pin = %s", (amount, self.current_pin))
                self.db.commit()
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!")
                self.create_menu_screen()
            else:
                messagebox.showerror("Error", "Insufficient balance.")
        else:
            messagebox.showerror("Error", "Invalid withdrawal amount.")

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the ATM GUI
root = tk.Tk()
atm = ATM_GUI(root)
root.mainloop()
