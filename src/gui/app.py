import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.styles import Styles
from src.gui.auth import AuthView
from src.gui.dashboard import DashboardView
from src.gui.analytics import AnalyticsView
from src.database import init_db
from src.exceptions import AppError

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Smart Expense Tracker")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        try:
            init_db()
        except AppError as e:
            messagebox.showerror("Database Error", str(e))
            self.destroy()
            return
            
        self.current_user = None
        self.current_theme = 'light'
        Styles.apply_theme(self, self.current_theme)
        
        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True)
        
        # Navbar (hidden initially)
        self.navbar = ttk.Frame(self)
        
        self.nav_title = ttk.Label(self.navbar, text="Smart Expense Tracker", font=('Segoe UI', 16, 'bold'))
        self.nav_title.pack(side='left', padx=10)
        
        self.user_lbl = ttk.Label(self.navbar, text="")
        self.user_lbl.pack(side='left', padx=10)
        
        self.theme_btn = ttk.Button(self.navbar, text="Toggle Theme", command=self.toggle_theme)
        self.theme_btn.pack(side='right', padx=5)
        
        self.logout_btn = ttk.Button(self.navbar, text="Logout", command=self.logout)
        self.logout_btn.pack(side='right', padx=5)
        
        # View tracking
        self.current_view = None
        self.notebook = None
        
        self.show_auth()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_auth(self):
        self.navbar.pack_forget()
        self.clear_container()
        self.current_view = AuthView(self.container, self)
        self.current_view.pack(fill='both', expand=True)

    def login_success(self, user):
        self.current_user = user
        self.current_theme = user.theme_preference
        Styles.apply_theme(self, self.current_theme)
        
        self.user_lbl.config(text=f"Welcome, {user.username}")
        self.navbar.pack(fill='x', side='top', pady=5)
        
        self.show_main_app()

    def show_main_app(self):
        self.clear_container()
        
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.dashboard_view = DashboardView(self.notebook, self.current_user, self)
        self.analytics_view = AnalyticsView(self.notebook, self.current_user)
        
        self.notebook.add(self.dashboard_view, text="Dashboard")
        self.notebook.add(self.analytics_view, text="Analytics")
        
        # Update chart when switching to analytics tab
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Analytics":
            self.analytics_view.update_chart()

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        Styles.apply_theme(self, self.current_theme)
        
        if self.current_user:
            try:
                self.current_user.update_theme(self.current_theme)
            except AppError as e:
                messagebox.showwarning("Warning", f"Could not save theme preference: {e}")

    def logout(self):
        self.current_user = None
        self.show_auth()
