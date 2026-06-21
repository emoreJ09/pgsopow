import tkinter as tk
from tkinter import messagebox
import db  # I-import ang db.py

class LoginScreen:
    def __init__(self, parent, on_login_success, on_go_to_signup):
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_go_to_signup = on_go_to_signup
        
        self.parent.title("Login - System")
        
        self.frame = tk.Frame(self.parent, padx=30, pady=30)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="ACCOUNT LOGIN", font=("Arial", 16, "bold"), fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(self.frame, text="Username:", font=("Arial", 11)).grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame, font=("Arial", 11), width=20)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)
        self.username_entry.focus()

        tk.Label(self.frame, text="Password:", font=("Arial", 11)).grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 11), width=20)
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        self.login_btn = tk.Button(self.frame, text="Login", command=self.handle_login, font=("Arial", 11, "bold"), bg="#2196F3", fg="white", cursor="hand2")
        self.login_btn.grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky="we")
        
        # Link papuntang Sign Up
        self.signup_lnk = tk.Button(self.frame, text="Don't have an account? Sign Up", command=self.on_go_to_signup, font=("Arial", 9, "underline"), fg="#2196F3", bd=0, bg=self.parent.cget("bg"), cursor="hand2")
        self.signup_lnk.grid(row=4, column=0, columnspan=2, pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Attention!", "All input fields must be filled out before proceeding")
            return

        user_role = db.authenticate_user(username, password)

        if user_role:
            messagebox.showinfo("Success!", f"Your credentials have been successfully verified.\nLogged in as {user_role.upper()}.")
            self.on_login_success(username, user_role)
        else:
            messagebox.showerror("Login Failed!", "Invalid username or password. Please try again.")


class RegisterScreen:
    def __init__(self, parent, on_go_to_login):
        self.parent = parent
        self.on_go_to_login = on_go_to_login
        
        self.parent.title("Sign Up - Create Account")
        
        self.frame = tk.Frame(self.parent, padx=30, pady=30)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="CREATE ACCOUNT", font=("Arial", 16, "bold"), fg="#4CAF50").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(self.frame, text="New Username:", font=("Arial", 11)).grid(row=1, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame, font=("Arial", 11), width=20)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)
        self.username_entry.focus()

        tk.Label(self.frame, text="New Password:", font=("Arial", 11)).grid(row=2, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 11), width=20)
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        self.register_btn = tk.Button(self.frame, text="Register Account", command=self.handle_register, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", cursor="hand2")
        self.register_btn.grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky="we")

        self.login_lnk = tk.Button(self.frame, text="Already have an account? Log In", command=self.on_go_to_login, font=("Arial", 9, "underline"), fg="#4CAF50", bd=0, bg=self.parent.cget("bg"), cursor="hand2")
        self.login_lnk.grid(row=4, column=0, columnspan=2, pady=5)

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Attention!", "All fields are required to register an account.")
            return

        success, message = db.register_user(username, password, role='encoder')
        
        if success:
            messagebox.showinfo("Success!", message)
            self.on_go_to_login()
        else:
            messagebox.showerror("Registration Failed!", message)