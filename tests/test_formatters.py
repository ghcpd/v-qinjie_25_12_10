"""
Tests for formatters.
"""

import unittest
import json
from user_display.formatters import BaseFormatter, CompactFormatter, JSONFormatter, TableFormatter

class TestFormatters(unittest.TestCase):

    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
        ]

    def test_base_formatter(self):
        formatter = BaseFormatter()
        result = formatter.format_users(self.users)
        lines = result.strip().split('\n')
        self.assertEqual(len(lines), 2)
        self.assertIn('ID=1', lines[0])
        self.assertIn('NAME=Alice', lines[0])

    def test_compact_formatter(self):
        formatter = CompactFormatter()
        result = formatter.format_users(self.users)
        lines = result.strip().split('\n')
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], '1: Alice')
        self.assertEqual(lines[1], '2: Bob')

    def test_json_formatter(self):
        formatter = JSONFormatter()
        result = formatter.format_users(self.users)
        parsed = json.loads(result)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['name'], 'Alice')

    def test_table_formatter(self):
        formatter = TableFormatter()
        result = formatter.format_users(self.users)
        lines = result.strip().split('\n')
        self.assertGreater(len(lines), 3)  # Header + separator + data
        self.assertIn('ID', lines[0])
        self.assertIn('NAME', lines[0])

if __name__ == '__main__':
    unittest.main()