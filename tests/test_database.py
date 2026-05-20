import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlite3
import src.database

# Use a test database
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_expenses.db')
src.database.DB_PATH = TEST_DB_PATH

from src.database import init_db, get_connection
from src.exceptions import DatabaseError

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Ensure fresh DB for each test
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except OSError:
                pass
            
    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            try:
                os.remove(TEST_DB_PATH)
            except PermissionError:
                pass

    def test_init_db(self):
        init_db()
        self.assertTrue(os.path.exists(TEST_DB_PATH))
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r['name'] for r in cursor.fetchall()]
            
            self.assertIn('users', tables)
            self.assertIn('categories', tables)
            self.assertIn('expenses', tables)
            self.assertIn('budgets', tables)
            self.assertIn('reports', tables)

if __name__ == '__main__':
    unittest.main()
