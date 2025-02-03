import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class ATM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("350x450")
        
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
        self.clear_window()
        
        tk.Label(self.root, text="Enter PIN:", font=("Arial", 14)).pack(pady=10)
        self.pin_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.pin_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.authenticate).pack(pady=10)
        tk.Button(self.root, text="Create Account", font=("Arial", 12), command=self.create_account_screen).pack(pady=5)

    def authenticate(self):
        pin = self.pin_entry.get()
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (pin,))
        result = self.cursor.fetchone()

        if result:
            self.current_pin = pin
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Incorrect PIN. Try again.")

    def create_account_screen(self):
        self.clear_window()
        
        tk.Label(self.root, text="Create New Account", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Set 4-digit PIN:", font=("Arial", 14)).pack()
        self.new_pin_entry = tk.Entry(self.root, font=("Arial", 14))
        self.new_pin_entry.pack(pady=5)
        
        tk.Button(self.root, text="Create", font=("Arial", 14), command=self.create_account).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.create_login_screen).pack(pady=5)
    
    def create_account(self):
        pin = self.new_pin_entry.get()
        if len(pin) == 4 and pin.isdigit():
            self.cursor.execute("INSERT INTO users (pin, balance) VALUES (%s, %s)", (pin, 0))
            self.db.commit()
            messagebox.showinfo("Success", "Account Created Successfully!")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "PIN must be a 4-digit number.")
    
    def create_menu_screen(self):
        self.clear_window()
        
        tk.Label(self.root, text="ATM Menu", font=("Arial", 16)).pack(pady=10)
        
        tk.Button(self.root, text="Check Balance", font=("Arial", 14), command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Deposit", font=("Arial", 14), command=self.deposit_screen).pack(pady=5)
        tk.Button(self.root, text="Withdraw", font=("Arial", 14), command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.root, text="Transaction History", font=("Arial", 14), command=self.transaction_history).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.create_login_screen).pack(pady=10)
    
    def check_balance(self):
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
        balance = self.cursor.fetchone()[0]
        messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")

    def deposit_screen(self):
        self.transaction_screen("Deposit")

    def withdraw_screen(self):
        self.transaction_screen("Withdraw")
    
    def transaction_screen(self, transaction_type):
        self.clear_window()
        
        tk.Label(self.root, text=f"Enter amount to {transaction_type.lower()}:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text=transaction_type, font=("Arial", 14), 
                  command=lambda: self.process_transaction(transaction_type)).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.create_menu_screen).pack(pady=5)
    
    def process_transaction(self, transaction_type):
        amount = self.amount_entry.get()
        if amount.isdigit() and float(amount) > 0:
            amount = float(amount)
            if transaction_type == "Withdraw":
                self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
                balance = self.cursor.fetchone()[0]
                if amount > balance:
                    messagebox.showerror("Error", "Insufficient balance.")
                    return
                self.cursor.execute("UPDATE users SET balance = balance - %s WHERE pin = %s", (amount, self.current_pin))
            else:
                self.cursor.execute("UPDATE users SET balance = balance + %s WHERE pin = %s", (amount, self.current_pin))
            
            self.cursor.execute("INSERT INTO transactions (pin, type, amount) VALUES (%s, %s, %s)",
                                (self.current_pin, transaction_type, amount))
            self.db.commit()
            messagebox.showinfo("Success", f"${amount:.2f} {transaction_type.lower()}ed successfully!")
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Invalid amount.")
    
    def transaction_history(self):
        self.clear_window()
        tk.Label(self.root, text="Transaction History", font=("Arial", 16)).pack(pady=10)
        
        self.cursor.execute("SELECT type, amount FROM transactions WHERE pin = %s", (self.current_pin,))
        transactions = self.cursor.fetchall()
        for t in transactions:
            tk.Label(self.root, text=f"{t[0]}: ${t[1]:.2f}", font=("Arial", 12)).pack()
        
        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.create_menu_screen).pack(pady=10)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
atm = ATM_GUI(root)
root.mainloop()
