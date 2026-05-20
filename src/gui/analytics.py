import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.models import Expense, Budget
from collections import defaultdict
from datetime import datetime

class AnalyticsView(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        
        # Top controls
        controls = ttk.Frame(self)
        controls.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(controls, text="Select Month:").pack(side='left', padx=(0, 5))
        
        self.month_var = tk.StringVar()
        self.months = [f"{m:02d}" for m in range(1, 13)]
        self.month_cb = ttk.Combobox(controls, textvariable=self.month_var, values=self.months, width=5, state="readonly")
        self.month_cb.pack(side='left', padx=(0, 10))
        
        ttk.Label(controls, text="Year:").pack(side='left', padx=(0, 5))
        self.year_var = tk.StringVar()
        current_year = datetime.now().year
        self.years = [str(y) for y in range(current_year-5, current_year+1)]
        self.year_cb = ttk.Combobox(controls, textvariable=self.year_var, values=self.years, width=6, state="readonly")
        self.year_cb.pack(side='left', padx=(0, 10))
        
        # Set defaults
        self.month_var.set(f"{datetime.now().month:02d}")
        self.year_var.set(str(current_year))
        
        ttk.Button(controls, text="Update Chart", command=self.update_chart).pack(side='left')
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Info labels
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(fill='x', padx=10, pady=(0, 10))
        self.total_label = ttk.Label(self.info_frame, text="Total Spent: $0.00", font=('Segoe UI', 14, 'bold'))
        self.total_label.pack(side='left', padx=20)
        self.budget_label = ttk.Label(self.info_frame, text="Budget Status: N/A", font=('Segoe UI', 14, 'bold'))
        self.budget_label.pack(side='right', padx=20)

    def update_chart(self):
        month = self.month_var.get()
        year = self.year_var.get()
        
        expenses = Expense.get_all(self.user.id)
        
        # Filter by month/year
        monthly_expenses = [e for e in expenses if e['date'].startswith(f"{year}-{month}")]
        
        category_totals = defaultdict(float)
        total_spent = 0.0
        
        for e in monthly_expenses:
            category_totals[e['category_name']] += e['amount']
            total_spent += e['amount']
            
        self.ax1.clear()
        self.ax2.clear()
        
        if category_totals:
            labels = list(category_totals.keys())
            sizes = list(category_totals.values())
            
            # Pie chart
            self.ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax1.axis('equal')
            self.ax1.set_title(f"Expenses by Category ({month}/{year})")
            
            # Bar chart
            self.ax2.bar(labels, sizes, color='#1890ff')
            self.ax2.set_title("Amount per Category")
            self.ax2.tick_params(axis='x', rotation=45)
        else:
            self.ax1.text(0.5, 0.5, 'No data for this month', ha='center', va='center')
            self.ax2.text(0.5, 0.5, 'No data for this month', ha='center', va='center')
            
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Update labels
        self.total_label.config(text=f"Total Spent: ${total_spent:.2f}")
        
        try:
            budget = Budget.get_budget(self.user.id, int(month), int(year))
            if budget > 0:
                remaining = budget - total_spent
                status = "Under Budget" if remaining >= 0 else "Over Budget!"
                color = "green" if remaining >= 0 else "red"
                self.budget_label.config(text=f"Budget: ${budget:.2f} | Remaining: ${remaining:.2f} ({status})")
            else:
                self.budget_label.config(text="No budget set for this month")
        except Exception as e:
            self.budget_label.config(text="Error loading budget")
