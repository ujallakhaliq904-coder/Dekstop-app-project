import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import src.database

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_expenses_models.db')
src.database.DB_PATH = TEST_DB_PATH

from src.database import init_db
from src.models import User, Category, Expense, Budget
from src.exceptions import AuthenticationError, ValidationError

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except OSError:
                pass
        init_db()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

    def test_1_user_registration_and_login(self):
        user = User.register("testuser", "password123")
        self.assertEqual(user.username, "testuser")
        
        with self.assertRaises(AuthenticationError):
            User.register("testuser", "newpass")
            
        logged_in = User.login("testuser", "password123")
        self.assertEqual(logged_in.id, user.id)
        
        with self.assertRaises(AuthenticationError):
            User.login("testuser", "wrongpass")

    def test_2_category_creation(self):
        user = User.login("testuser", "password123")
        cat = Category.create(user.id, "TestCategory")
        self.assertEqual(cat.name, "TestCategory")
        
        with self.assertRaises(ValidationError):
            Category.create(user.id, "TestCategory")
            
        cats = Category.get_all(user.id)
        self.assertTrue(any(c.name == "TestCategory" for c in cats))

    def test_3_expense_management(self):
        user = User.login("testuser", "password123")
        cat = Category.get_all(user.id)[0]
        
        exp = Expense.add(user.id, cat.id, 50.5, "2023-10-01", "Test Expense")
        self.assertEqual(exp.amount, 50.5)
        
        with self.assertRaises(ValidationError):
            Expense.add(user.id, cat.id, -10, "2023-10-01", "Invalid")
            
        expenses = Expense.get_all(user.id)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]['description'], "Test Expense")
        
        Expense.update(exp.id, 60.0, "2023-10-02", "Updated Expense", cat.id)
        updated = Expense.get_all(user.id)[0]
        self.assertEqual(updated['amount'], 60.0)
        self.assertEqual(updated['description'], "Updated Expense")
        
        Expense.delete(exp.id)
        self.assertEqual(len(Expense.get_all(user.id)), 0)

    def test_4_budget(self):
        user = User.login("testuser", "password123")
        Budget.set_budget(user.id, 10, 2023, 1000.0)
        
        val = Budget.get_budget(user.id, 10, 2023)
        self.assertEqual(val, 1000.0)
        
        # Test update
        Budget.set_budget(user.id, 10, 2023, 1500.0)
        val = Budget.get_budget(user.id, 10, 2023)
        self.assertEqual(val, 1500.0)

if __name__ == '__main__':
    unittest.main()
