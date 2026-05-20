import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import os
import csv
from src.utils import export_to_csv

class TestUtils(unittest.TestCase):
    def test_export_to_csv(self):
        test_file = os.path.join(os.path.dirname(__file__), 'test_export.csv')
        if os.path.exists(test_file):
            os.remove(test_file)
            
        mock_data = [
            {'date': '2023-10-01', 'category_name': 'Food', 'amount': 15.5, 'description': 'Lunch'},
            {'date': '2023-10-02', 'category_name': 'Transport', 'amount': 5.0, 'description': 'Bus'}
        ]
        
        export_to_csv(mock_data, test_file)
        self.assertTrue(os.path.exists(test_file))
        
        with open(test_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3) # Header + 2 data rows
            self.assertEqual(rows[0], ['Date', 'Category', 'Amount', 'Description'])
            self.assertEqual(rows[1], ['2023-10-01', 'Food', '15.50', 'Lunch'])
            
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
