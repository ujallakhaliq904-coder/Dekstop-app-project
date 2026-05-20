import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hashlib
import sqlite3
from datetime import datetime
from src.database import get_connection
from src.exceptions import AuthenticationError, DatabaseError, ValidationError

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

class User:
    def __init__(self, id, username, theme_preference='light'):
        self.id = id
        self.username = username
        self.theme_preference = theme_preference

    @classmethod
    def register(cls, username, password):
        if not username or not password:
            raise ValidationError("Username and password cannot be empty.")
            
        hashed_pw = hash_password(password)
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)", 
                    (username, hashed_pw)
                )
                conn.commit()
                return cls(cursor.lastrowid, username)
        except sqlite3.IntegrityError:
            raise AuthenticationError("Username already exists.")
        except sqlite3.Error as e:
            raise DatabaseError(f"Registration failed: {e}")

    @classmethod
    def login(cls, username, password):
        if not username or not password:
            raise ValidationError("Username and password cannot be empty.")
            
        hashed_pw = hash_password(password)
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, username, theme_preference FROM users WHERE username=? AND password=?",
                    (username, hashed_pw)
                )
                row = cursor.fetchone()
                if row:
                    return cls(row['id'], row['username'], row['theme_preference'])
                else:
                    raise AuthenticationError("Invalid username or password.")
        except sqlite3.Error as e:
            raise DatabaseError(f"Login failed: {e}")

    def update_theme(self, theme):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET theme_preference=? WHERE id=?", 
                    (theme, self.id)
                )
                conn.commit()
                self.theme_preference = theme
        except sqlite3.Error as e:
            raise DatabaseError(f"Theme update failed: {e}")

class Category:
    def __init__(self, id, user_id, name):
        self.id = id
        self.user_id = user_id
        self.name = name

    @classmethod
    def create(cls, user_id, name):
        if not name:
            raise ValidationError("Category name cannot be empty.")
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO categories (user_id, name) VALUES (?, ?)",
                    (user_id, name)
                )
                conn.commit()
                return cls(cursor.lastrowid, user_id, name)
        except sqlite3.IntegrityError:
            raise ValidationError(f"Category '{name}' already exists.")
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to create category: {e}")

    @classmethod
    def get_all(cls, user_id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM categories WHERE user_id=?", (user_id,))
                return [cls(r['id'], r['user_id'], r['name']) for r in cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to get categories: {e}")
            
    @classmethod
    def initialize_defaults(cls, user_id):
        defaults = ["Food", "Transport", "Utilities", "Entertainment", "Healthcare", "Other"]
        for cat in defaults:
            try:
                cls.create(user_id, cat)
            except ValidationError:
                pass # Already exists

class Expense:
    def __init__(self, id, user_id, category_id, amount, date, description):
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.date = date
        self.description = description

    @classmethod
    def add(cls, user_id, category_id, amount, date, description):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            raise ValidationError("Amount must be a positive number.")
            
        if not date:
            raise ValidationError("Date is required.")
            
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expenses (user_id, category_id, amount, date, description) VALUES (?, ?, ?, ?, ?)",
                    (user_id, category_id, amount, date, description)
                )
                conn.commit()
                return cls(cursor.lastrowid, user_id, category_id, amount, date, description)
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to add expense: {e}")

    @classmethod
    def update(cls, id, amount, date, description, category_id):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            raise ValidationError("Amount must be a positive number.")
            
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE expenses SET amount=?, date=?, description=?, category_id=? WHERE id=?",
                    (amount, date, description, category_id, id)
                )
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to update expense: {e}")

    @classmethod
    def delete(cls, id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to delete expense: {e}")

    @classmethod
    def get_all(cls, user_id, search_term=None, category_id=None):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT e.*, c.name as category_name 
                    FROM expenses e 
                    JOIN categories c ON e.category_id = c.id 
                    WHERE e.user_id=?
                """
                params = [user_id]
                
                if category_id:
                    query += " AND e.category_id=?"
                    params.append(category_id)
                    
                if search_term:
                    query += " AND (e.description LIKE ? OR c.name LIKE ?)"
                    params.append(f"%{search_term}%")
                    params.append(f"%{search_term}%")
                    
                query += " ORDER BY e.date DESC"
                
                cursor.execute(query, tuple(params))
                return cursor.fetchall() # Returning raw rows for GUI table ease
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to fetch expenses: {e}")

class Budget:
    @classmethod
    def set_budget(cls, user_id, month, year, amount):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError()
        except ValueError:
            raise ValidationError("Budget amount must be a non-negative number.")
            
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                # Upsert
                cursor.execute("""
                    INSERT INTO budgets (user_id, month, year, amount)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id, month, year) 
                    DO UPDATE SET amount=excluded.amount
                """, (user_id, month, year, amount))
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to set budget: {e}")

    @classmethod
    def get_budget(cls, user_id, month, year):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT amount FROM budgets WHERE user_id=? AND month=? AND year=?",
                    (user_id, month, year)
                )
                row = cursor.fetchone()
                return row['amount'] if row else 0.0
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to get budget: {e}")
