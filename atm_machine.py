import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import mysql.connector
import datetime as dt
import pygame as py

class ATM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("400x500")
        self.root.configure(bg="#222831")  # Dark background for contrast

        self.languages = {
            "English": {
                "menu": "ATM Menu",
                "check_balance": "Check Balance",
                "deposit": "Deposit",
                "withdraw": "Withdraw",
                "transaction_history": "Transaction History",
                "update_pin": "Update PIN",
                "update_profile": "Update Profile",
                "delete_account": "Delete Account",
                "transfer_money": "Transfer Money",
                "exit": "Exit",
                "enter_pin": "Enter PIN:",
                "login": "Login",
                "create_account": "Create Account",
                "success": "Success",
                "error": "Error",
                "balance": "Your balance is: $",
                "enter_amount": "Enter amount:",
                "insufficient_balance": "Insufficient balance.",
                "transaction_success": "Transaction successful!",
                "back": "Back",
                "enter_current_pin": "Enter Current PIN:",
                "enter_new_pin": "Enter New PIN:",
                "confirm_new_pin": "Confirm New PIN:",
                "confirm_delete": "Are you sure you want to delete your account?",
                "update_username": "Enter New Username:",
                "update_phone": "Enter New Phone Number:",
                "enter_destination": "Enter Destination Account PIN:",
                "enter_transfer_amount": "Enter amount to transfer:",
                "transfer_success": "Money transferred successfully!",
                "transfer_failed": "Transfer failed! Destination account not found."
            },
            "Spanish": {
                "menu": "Menú del Cajero",
                "check_balance": "Consultar Saldo",
                "deposit": "Depósito",
                "withdraw": "Retirar",
                "transaction_history": "Historial de Transacciones",
                "update_pin": "Actualizar PIN",
                "update_profile": "Actualizar Perfil",
                "delete_account": "Eliminar Cuenta",
                "transfer_money": "Transferir Dinero",
                "exit": "Salir",
                "enter_pin": "Ingrese PIN:",
                "login": "Iniciar Sesión",
                "create_account": "Crear Cuenta",
                "success": "Éxito",
                "error": "Error",
                "balance": "Su saldo es: $",
                "enter_amount": "Ingrese cantidad:",
                "insufficient_balance": "Saldo insuficiente.",
                "transaction_success": "¡Transacción exitosa!",
                "back": "Atrás",
                "enter_current_pin": "Ingrese PIN Actual:",
                "enter_new_pin": "Ingrese Nuevo PIN:",
                "confirm_new_pin": "Confirme Nuevo PIN:",
                "confirm_delete": "¿Está seguro de que desea eliminar su cuenta?",
                "update_username": "Ingrese Nuevo Nombre de Usuario:",
                "update_phone": "Ingrese Nuevo Número de Teléfono:",
                "enter_destination": "Ingrese el PIN de la cuenta de destino:",
                "enter_transfer_amount": "Ingrese la cantidad a transferir:",
                "transfer_success": "¡Dinero transferido exitosamente!",
                "transfer_failed": "¡Transferencia fallida! Cuenta de destino no encontrada."
            },
            "Hindi": {
                "menu": "एटीएम मेनू",
                "check_balance": "बैलेंस देखें",
                "deposit": "जमा करें",
                "withdraw": "निकालें",
                "transaction_history": "लेन-देन इतिहास",
                "update_pin": "पिन अपडेट करें",
                "update_profile": "प्रोफ़ाइल अपडेट करें",
                "delete_account": "खाता हटाएं",
                "transfer_money": "पैसे ट्रांसफर करें",
                "exit": "बाहर जाएं",
                "enter_pin": "पिन दर्ज करें:",
                "login": "लॉगिन करें",
                "create_account": "खाता बनाएं",
                "success": "सफलता",
                "error": "त्रुटि",
                "balance": "आपका बैलेंस है: $",
                "enter_amount": "राशि दर्ज करें:",
                "insufficient_balance": "पर्याप्त बैलेंस नहीं है।",
                "transaction_success": "लेन-देन सफल!",
                "back": "वापस",
                "enter_current_pin": "वर्तमान पिन दर्ज करें:",
                "enter_new_pin": "नया पिन दर्ज करें:",
                "confirm_new_pin": "नया पिन पुष्टि करें:",
                "confirm_delete": "क्या आप वाकई अपना खाता हटाना चाहते हैं?",
                "update_username": "नया उपयोगकर्ता नाम दर्ज करें:",
                "update_phone": "नया फ़ोन नंबर दर्ज करें:",
                "enter_destination": "गंतव्य खाता पिन दर्ज करें:",
                "enter_transfer_amount": "स्थानांतरण करने के लिए राशि दर्ज करें:",
                "transfer_success": "पैसे सफलतापूर्वक ट्रांसफर हो गए!",
                "transfer_failed": "ट्रांसफर विफल रहा! गंतव्य खाता नहीं मिला।"
            }
        }
        
        self.current_language = "English"
        
        # Establish Database Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="Mayank",
            password="Rcf@634e",  
            database="atm_db"
        )
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#222831")
        self.style.configure("TLabel", background="#222831", foreground="#EEEEEE", font=("Arial", 14))
        self.style.configure("TButton", font=("Arial", 12), padding=5, background="#00ADB5", foreground="black")

        
        self.cursor = self.db.cursor()

        self.current_pin = None
        self.create_language_selection_screen()
    
       # self.create_login_screen()

    def create_language_selection_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Select Language:", font=("Arial", 14)).pack(pady=10)
        self.language_var = tk.StringVar(value=self.current_language)
        for lang in self.languages.keys():
            ttk.Radiobutton(frame, text=lang, variable=self.language_var, value=lang, command=self.update_language).pack(pady=2)
        
        ttk.Button(frame, text="Continue", command=self.create_login_screen).pack(pady=10)
    
    
    def update_language(self):
        self.current_language = self.language_var.get()

    def create_login_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        lang_text = self.languages[self.current_language]
        ttk.Label(frame, text=lang_text["enter_pin"], font=("Arial", 14)).pack(pady=10)
        self.pin_entry = ttk.Entry(frame, show="*", font=("Arial", 14), background="#393E46", foreground="black")
        self.pin_entry.pack(pady=5)
        
        ttk.Button(frame, text=lang_text["login"], command=self.authenticate).pack(pady=10)
        ttk.Button(frame, text=lang_text["create_account"], command=self.create_account_screen).pack(pady=5)
        ttk.Button(frame, text=lang_text["back"], command=self.create_language_selection_screen).pack(pady=5)
    
    def create_menu_screen(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        lang_text = self.languages[self.current_language]
        ttk.Label(frame, text=lang_text["menu"], font=("Arial", 16)).pack(pady=10)
        
        ttk.Button(frame, text=lang_text["check_balance"], command=self.check_balance).pack(pady=5)
        ttk.Button(frame, text=lang_text["deposit"], command=self.deposit_screen).pack(pady=5)
        ttk.Button(frame, text=lang_text["withdraw"], command=self.withdraw_screen).pack(pady=5)
        ttk.Button(frame, text=lang_text["transaction_history"], command=self.transaction_history).pack(pady=5)
        
        # Adding buttons for account management
        ttk.Button(frame, text=lang_text["update_pin"], command=self.update_pin_screen).pack(pady=5)
        ttk.Button(frame, text=lang_text["delete_account"], command=self.delete_account_screen).pack(pady=5)

        ttk.Button(frame, text=lang_text["transfer_money"], command=self.transfer_money_screen).pack(pady=5)
        ttk.Button(frame, text=lang_text["exit"], command=self.create_login_screen).pack(pady=10)
    
    def delete_account_screen(self):
        self.clear_window()
        lang_text = self.languages[self.current_language]
        
        ttk.Label(self.root, text=lang_text["enter_current_pin"], font=("Arial", 14)).pack(pady=5)
        current_pin_entry = ttk.Entry(self.root, show='*')
        current_pin_entry.pack(pady=5)
        
        def delete_account():
            current_pin_value = current_pin_entry.get()
            if current_pin_value == self.current_pin:
                response = messagebox.askyesno(lang_text["delete_account"], lang_text["confirm_delete"])
                if response:
                    self.cursor.execute("DELETE FROM transactions WHERE pin = %s", (self.current_pin,))
                    self.cursor.execute("DELETE FROM users WHERE pin = %s", (self.current_pin,))
                    self.db.commit()
                    messagebox.showinfo(lang_text["success"], "Account deleted successfully!")
                    self.current_pin = None
                    self.create_language_selection_screen()
            else:
                messagebox.showerror(lang_text["error"], "Incorrect PIN!")
        
        ttk.Button(self.root, text=lang_text["delete_account"], command=delete_account).pack(pady=10)
        ttk.Button(self.root, text=lang_text["back"], command=self.create_menu_screen).pack(pady=10)
    
    def authenticate(self):
        lang_text = self.languages[self.current_language]
        pin = self.pin_entry.get()
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (pin,))
        result = self.cursor.fetchone()

        if result:
            self.current_pin = pin
            self.create_menu_screen()
        else:
            messagebox.showerror(lang_text["error"], "Incorrect PIN. Try again.")

    def create_account_screen(self):
        lang_text = self.languages[self.current_language]
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Create New Account", font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame, text="Set 4-digit PIN:", font=("Arial", 14)).pack()
        self.new_pin_entry = ttk.Entry(frame, show='*', font=("Arial", 14), background="#393E46", foreground="black")
        self.new_pin_entry.pack(pady=5)
        
        ttk.Button(frame, text=lang_text['create_account'], command=self.create_account).pack(pady=10)
        ttk.Button(frame, text=lang_text["Back"], command=self.create_login_screen).pack(pady=5)
    
    def create_account(self):
        lang_text = self.languages[self.current_language]
        pin = self.new_pin_entry.get()
        if len(pin) == 4 and pin.isdigit():
            self.cursor.execute("INSERT INTO users (pin, balance) VALUES (%s, %s)", (pin, 0))
            self.db.commit()
            messagebox.showinfo(lang_text["success"], "Account Created Successfully!")
            self.create_login_screen()
        else:
            messagebox.showerror(lang_text["error"], "PIN must be a 4-digit number.")
    
    
    def check_balance(self):
        lang_text = self.languages[self.current_language]
        self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
        balance = self.cursor.fetchone()[0]
        messagebox.showinfo(lang_text["balance"], f"${balance:.2f}")

    def deposit_screen(self):
        self.transaction_screen("Deposit")

    def withdraw_screen(self):
        self.transaction_screen("Withdraw")
    
    def transaction_screen(self, transaction_type):
        self.clear_window()
        lang_text = self.languages[self.current_language]
        if(transaction_type == 'Deposit'):
            key = lang_text['deposit']
        else:
            key = lang_text['withdraw']
        tk.Label(self.root, text=f"{key}:", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"{lang_text['enter_amount']}:", font=("Arial", 14)).pack(pady=10)
        self.amount_entry = tk.Entry(self.root, font=("Arial", 14))
        self.amount_entry.pack(pady=5)
        
        tk.Button(self.root, text=transaction_type, font=("Arial", 14), 
                  command=lambda: self.process_transaction(transaction_type)).pack(pady=10)
        tk.Button(self.root, text="Back", font=("Arial", 12), command=self.create_menu_screen).pack(pady=5)
    
    def process_transaction(self, transaction_type):

        lang_text = self.languages[self.current_language]
        amount = self.amount_entry.get()
        sound_file ="./venv/Resources/audio/transaction_sound.mp3"
        error_sound ="./venv/Resources/audio/error.mp3"
        if amount.isdigit() and float(amount) > 0:
            amount = float(amount)
            if transaction_type == "Withdraw":
                self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
                balance = self.cursor.fetchone()[0]
                if amount > balance:
                    messagebox.showerror(self.lang_text['error'], self.lang_text["insufficient_balance"])
                    return
                self.cursor.execute("UPDATE users SET balance = balance - %s WHERE pin = %s", (amount, self.current_pin))
            else:
                self.cursor.execute("UPDATE users SET balance = balance + %s WHERE pin = %s", (amount, self.current_pin))
            
            self.cursor.execute(
             "INSERT INTO transactions (pin, type, amount, timestamp) VALUES (%s, %s, %s, NOW())",
            (self.current_pin, transaction_type, amount))
            self.db.commit()

            # Play transaction sound
            py.mixer.init()
            py.mixer.music.load(sound_file)
            py.mixer.music.play()

            messagebox.showinfo(lang_text['success'], f"${amount:.2f} {transaction_type.lower()}ed successfully!")
            self.create_menu_screen()
        else:
            py.mixer.init()
            py.mixer.music.load(error_sound)
            py.mixer.music.play()
            messagebox.showerror(lang_text['error'], "Invalid amount.")
    
    def transaction_history(self):
        self.clear_window()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        lang_text = self.languages[self.current_language]
        ttk.Label(frame, text=lang_text["transaction_history"], font=("Arial", 16)).pack(pady=10)
        
        self.cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE pin = %s ORDER BY timestamp DESC", (self.current_pin,))
        transactions = self.cursor.fetchall()
        
        if not transactions:
            ttk.Label(frame, text="No Transactions!", font=("Arial", 12)).pack(pady=5)
        else:
            tree = ttk.Treeview(frame, columns=("Type", "Amount", "Date"), show="headings")
            tree.heading("Type", text="Type")
            tree.heading("Amount", text="Amount ($)")
            tree.heading("Date", text="Date")
            tree.column("Type", anchor="center", width=100)
            tree.column("Amount", anchor="center", width=100)
            tree.column("Date", anchor="center", width=150)
            
            for t in transactions:
                tree.insert("", "end", values=(t[0], f"${t[1]:.2f}", t[2]))
            
            tree.pack(pady=10)
        
        ttk.Button(frame, text=lang_text["back"], command=self.create_menu_screen).pack(pady=10)
    
    def update_pin_screen(self):
        self.clear_window()
        lang_text = self.languages[self.current_language]
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=lang_text["update_pin"], font=("Arial", 16)).pack(pady=10)

        # Current PIN field
        ttk.Label(frame, text=lang_text["enter_current_pin"]).pack(pady=5)
        self.current_pin_entry = ttk.Entry(frame, show="*")
        self.current_pin_entry.pack(pady=5)

        # New PIN field
        ttk.Label(frame, text=lang_text["enter_new_pin"]).pack(pady=5)
        self.new_pin_entry = ttk.Entry(frame, show="*")
        self.new_pin_entry.pack(pady=5)

        # Confirm New PIN field
        ttk.Label(frame, text=lang_text["confirm_new_pin"]).pack(pady=5)
        self.confirm_pin_entry = ttk.Entry(frame, show="*")
        self.confirm_pin_entry.pack(pady=5)

        ttk.Button(frame, text=lang_text["update_pin"], command=self.update_pin).pack(pady=10)
        ttk.Button(frame, text=lang_text['back'], command=self.create_menu_screen).pack(pady=10)

    def update_pin(self):
        lang_text = self.languages[self.current_language]
        
        # Get user input
        current_pin_value = self.current_pin_entry.get()
        new_pin_value = self.new_pin_entry.get()
        confirm_pin_value = self.confirm_pin_entry.get()

        if new_pin_value != confirm_pin_value:
            messagebox.showerror(lang_text["error"], "New PINs do not match!")
            return

        # Validate current PIN
        self.cursor.execute("SELECT * FROM users WHERE pin = %s", (current_pin_value,))
        user = self.cursor.fetchone()

        if user:
            self.cursor.execute("UPDATE users SET pin = %s WHERE pin = %s", (new_pin_value, current_pin_value))
            self.db.commit()
            messagebox.showinfo(lang_text["success"], "PIN updated successfully!")
            self.create_menu_screen()
        else:
            messagebox.showerror(lang_text["error"], "Incorrect current PIN")

    def transfer_money_screen(self):
        self.clear_window()
        lang_text = self.languages[self.current_language]
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text=lang_text["transfer_money"], font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame, text=lang_text["enter_destination"], font=("Arial", 14)).pack(pady=5)
        destination_entry = ttk.Entry(frame)
        destination_entry.pack(pady=5)
        
        ttk.Label(frame, text=lang_text["enter_transfer_amount"], font=("Arial", 14)).pack(pady=5)
        amount_entry = ttk.Entry(frame)
        amount_entry.pack(pady=5)
        
        def process_transfer():
            dest_pin = destination_entry.get()
            amount_str = amount_entry.get()
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(lang_text["error"], lang_text["enter_amount"])
                return
            
            # Check if destination account exists
            self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (dest_pin,))
            dest_user = self.cursor.fetchone()
            if not dest_user:
                messagebox.showerror(lang_text["error"], lang_text["transfer_failed"])
                return
            
            # Check if current user has enough funds
            self.cursor.execute("SELECT balance FROM users WHERE pin = %s", (self.current_pin,))
            current_balance = self.cursor.fetchone()[0]
            if amount > current_balance:
                messagebox.showerror(lang_text["error"], lang_text["insufficient_balance"])
                return
            
            # Perform transfer: deduct from current user and add to destination user
            self.cursor.execute("UPDATE users SET balance = balance - %s WHERE pin = %s", (amount, self.current_pin))
            self.cursor.execute("UPDATE users SET balance = balance + %s WHERE pin = %s", (amount, dest_pin))
            self.db.commit()
            messagebox.showinfo(lang_text["success"], lang_text["transfer_success"])
            self.create_menu_screen()
        
        ttk.Button(frame, text=lang_text["transfer_money"], command=process_transfer).pack(pady=10)
        ttk.Button(frame, text=lang_text["back"], command=self.create_menu_screen).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
atm = ATM_GUI(root)
root.mainloop()
