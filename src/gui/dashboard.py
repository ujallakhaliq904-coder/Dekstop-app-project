import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from src.models import Expense, Category, Budget
from src.utils import export_to_csv
from src.exceptions import AppError

class DashboardView(ttk.Frame):
    def __init__(self, parent, user, controller):
        super().__init__(parent)
        self.user = user
        self.controller = controller
        
        Category.initialize_defaults(self.user.id)
        
        # Left Panel (Forms)
        self.left_panel = ttk.Frame(self, width=300, padding=10)
        self.left_panel.pack(side='left', fill='y')
        
        self.setup_expense_form()
        self.setup_budget_form()
        
        # Right Panel (List and Actions)
        self.right_panel = ttk.Frame(self, padding=10)
        self.right_panel.pack(side='right', fill='both', expand=True)
        
        self.setup_list_view()
        
        self.load_categories()
        self.refresh_list()

    def setup_expense_form(self):
        form = ttk.LabelFrame(self.left_panel, text="Add/Edit Expense", padding=10)
        form.pack(fill='x', pady=(0, 10))
        
        ttk.Label(form, text="Amount:").pack(anchor='w')
        self.amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.amount_var).pack(fill='x', pady=(0, 5))
        
        ttk.Label(form, text="Category:").pack(anchor='w')
        self.category_var = tk.StringVar()
        self.category_cb = ttk.Combobox(form, textvariable=self.category_var, state="readonly")
        self.category_cb.pack(fill='x', pady=(0, 5))
        
        ttk.Label(form, text="Date (YYYY-MM-DD):").pack(anchor='w')
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form, textvariable=self.date_var).pack(fill='x', pady=(0, 5))
        
        ttk.Label(form, text="Description:").pack(anchor='w')
        self.desc_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.desc_var).pack(fill='x', pady=(0, 10))
        
        self.editing_id = None
        
        btn_frame = ttk.Frame(form)
        btn_frame.pack(fill='x')
        self.save_btn = ttk.Button(btn_frame, text="Save Expense", command=self.save_expense, style='Accent.TButton')
        self.save_btn.pack(side='left', expand=True, fill='x', padx=(0, 2))
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side='right', expand=True, fill='x', padx=(2, 0))

    def setup_budget_form(self):
        form = ttk.LabelFrame(self.left_panel, text="Set Monthly Budget", padding=10)
        form.pack(fill='x')
        
        frame = ttk.Frame(form)
        frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(frame, text="Month:").pack(side='left')
        self.b_month_var = tk.StringVar(value=f"{datetime.now().month:02d}")
        ttk.Combobox(frame, textvariable=self.b_month_var, values=[f"{m:02d}" for m in range(1, 13)], width=3).pack(side='left', padx=5)
        
        ttk.Label(frame, text="Year:").pack(side='left')
        self.b_year_var = tk.StringVar(value=str(datetime.now().year))
        ttk.Entry(frame, textvariable=self.b_year_var, width=5).pack(side='left', padx=5)
        
        ttk.Label(form, text="Amount:").pack(anchor='w')
        self.b_amount_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.b_amount_var).pack(fill='x', pady=(0, 10))
        
        ttk.Button(form, text="Set Budget", command=self.set_budget).pack(fill='x')

    def setup_list_view(self):
        # Toolbar
        toolbar = ttk.Frame(self.right_panel)
        toolbar.pack(fill='x', pady=(0, 10))
        
        ttk.Label(toolbar, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.refresh_list())
        ttk.Entry(toolbar, textvariable=self.search_var).pack(side='left', padx=(5, 20))
        
        ttk.Button(toolbar, text="Export CSV", command=self.export_data).pack(side='right', padx=5)
        ttk.Button(toolbar, text="Delete Selected", command=self.delete_expense).pack(side='right', padx=5)
        ttk.Button(toolbar, text="Edit Selected", command=self.edit_expense).pack(side='right', padx=5)
        
        # Table
        columns = ("id", "date", "category", "amount", "description")
        self.tree = ttk.Treeview(self.right_panel, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount ($)")
        self.tree.heading("description", text="Description")
        
        self.tree.column("id", width=0, stretch=False) # Hide ID
        self.tree.column("date", width=100)
        self.tree.column("category", width=120)
        self.tree.column("amount", width=100)
        self.tree.column("description", width=250)
        
        scrollbar = ttk.Scrollbar(self.right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def load_categories(self):
        try:
            self.categories = Category.get_all(self.user.id)
            self.category_cb['values'] = [c.name for c in self.categories]
            if self.categories:
                self.category_cb.set(self.categories[0].name)
        except AppError as e:
            messagebox.showerror("Error", str(e))

    def get_category_id(self, name):
        for c in self.categories:
            if c.name == name:
                return c.id
        return None

    def save_expense(self):
        amount = self.amount_var.get()
        date = self.date_var.get()
        desc = self.desc_var.get()
        cat_name = self.category_var.get()
        cat_id = self.get_category_id(cat_name)
        
        if not cat_id:
            messagebox.showerror("Error", "Please select a category")
            return
            
        try:
            if self.editing_id:
                Expense.update(self.editing_id, amount, date, desc, cat_id)
                self.editing_id = None
                self.save_btn.config(text="Save Expense")
            else:
                Expense.add(self.user.id, cat_id, amount, date, desc)
            self.clear_form()
            self.refresh_list()
            messagebox.showinfo("Success", "Expense saved successfully")
            if hasattr(self.controller, 'analytics_view'):
                self.controller.analytics_view.update_chart()
        except AppError as e:
            messagebox.showerror("Error", str(e))

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to edit")
            return
            
        item = self.tree.item(selected[0])['values']
        self.editing_id = item[0]
        self.date_var.set(item[1])
        self.category_var.set(item[2])
        self.amount_var.set(str(item[3]))
        self.desc_var.set(item[4])
        self.save_btn.config(text="Update Expense")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this expense?"):
            item_id = self.tree.item(selected[0])['values'][0]
            try:
                Expense.delete(item_id)
                self.refresh_list()
                if hasattr(self.controller, 'analytics_view'):
                    self.controller.analytics_view.update_chart()
            except AppError as e:
                messagebox.showerror("Error", str(e))

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        search = self.search_var.get()
        try:
            expenses = Expense.get_all(self.user.id, search_term=search if search else None)
            for e in expenses:
                self.tree.insert("", "end", values=(
                    e['id'], e['date'], e['category_name'], f"{e['amount']:.2f}", e['description']
                ))
        except AppError as e:
            messagebox.showerror("Error", str(e))

    def clear_form(self):
        self.amount_var.set("")
        self.desc_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.editing_id = None
        self.save_btn.config(text="Save Expense")

    def set_budget(self):
        month = self.b_month_var.get()
        year = self.b_year_var.get()
        amount = self.b_amount_var.get()
        
        try:
            Budget.set_budget(self.user.id, int(month), int(year), amount)
            messagebox.showinfo("Success", "Budget updated successfully")
            if hasattr(self.controller, 'analytics_view'):
                self.controller.analytics_view.update_chart()
        except AppError as e:
            messagebox.showerror("Error", str(e))
        except ValueError:
            messagebox.showerror("Error", "Invalid month or year")

    def export_data(self):
        expenses = Expense.get_all(self.user.id)
        if not expenses:
            messagebox.showinfo("Info", "No data to export")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        if filepath:
            try:
                export_to_csv(expenses, filepath)
                messagebox.showinfo("Success", f"Data exported to {filepath}")
            except AppError as e:
                messagebox.showerror("Error", str(e))
