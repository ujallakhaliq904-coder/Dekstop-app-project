import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import os
from datetime import datetime
from src.exceptions import ExportError

def export_to_csv(expenses, filepath):
    """
    Export a list of expenses to a CSV file.
    expenses: List of sqlite3.Row objects from Expense.get_all
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
            
            for exp in expenses:
                writer.writerow([
                    exp['date'],
                    exp['category_name'],
                    f"{exp['amount']:.2f}",
                    exp['description']
                ])
    except IOError as e:
        raise ExportError(f"Failed to write to file: {e}")
