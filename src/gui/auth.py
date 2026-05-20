import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from src.models import User
from src.exceptions import AppError

class AuthView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Center container
        self.container = ttk.Frame(self, style='Card.TFrame', padding=30)
        self.container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.title_label = ttk.Label(self.container, text="Smart Expense Tracker", style='Header.TLabel')
        self.title_label.pack(pady=(0, 20))
        
        self.mode = 'login' # 'login' or 'register'
        
        # Form fields
        ttk.Label(self.container, text="Username:", style='Card.TLabel').pack(anchor='w')
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.container, textvariable=self.username_var, width=30)
        self.username_entry.pack(pady=(0, 10))
        
        ttk.Label(self.container, text="Password:", style='Card.TLabel').pack(anchor='w')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.container, textvariable=self.password_var, width=30, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        # Buttons
        self.action_btn = ttk.Button(self.container, text="Login", command=self.handle_action, style='Accent.TButton')
        self.action_btn.pack(fill='x', pady=(0, 10))
        
        self.switch_btn = ttk.Button(self.container, text="Need an account? Register", command=self.switch_mode)
        self.switch_btn.pack(fill='x')

    def switch_mode(self):
        if self.mode == 'login':
            self.mode = 'register'
            self.action_btn.config(text="Register")
            self.switch_btn.config(text="Already have an account? Login")
        else:
            self.mode = 'login'
            self.action_btn.config(text="Login")
            self.switch_btn.config(text="Need an account? Register")

    def handle_action(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
            
        try:
            if self.mode == 'login':
                user = User.login(username, password)
                self.controller.login_success(user)
            else:
                user = User.register(username, password)
                messagebox.showinfo("Success", "Registration successful. You are now logged in.")
                self.controller.login_success(user)
        except AppError as e:
            messagebox.showerror("Error", str(e))
