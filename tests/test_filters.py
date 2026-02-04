"""
Tests for filters.
"""

import unittest
from user_display.filters import BaseFilter, RegexFilter, CompositeFilter

class TestFilters(unittest.TestCase):

    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'User'},
        ]

    def test_base_filter_exact(self):
        filter_obj = BaseFilter({'role': 'Admin'})
        matches = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'Alice')

    def test_base_filter_case_insensitive(self):
        filter_obj = BaseFilter({'name': 'alice'}, case_sensitive=False)
        matches = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matches), 1)

    def test_regex_filter(self):
        filter_obj = RegexFilter({'name': r'Alice.*'})
        matches = [u for u in self.users if filter_obj.matches(u)]
        self.assertEqual(len(matches), 1)

    def test_composite_filter_and(self):
        f1 = BaseFilter({'role': 'User'})
        f2 = BaseFilter({'name': 'Bob'})
        composite = CompositeFilter([f1, f2], 'AND')
        matches = [u for u in self.users if composite.matches(u)]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['name'], 'Bob')

    def test_composite_filter_or(self):
        f1 = BaseFilter({'role': 'Admin'})
        f2 = BaseFilter({'name': 'Bob'})
        composite = CompositeFilter([f1, f2], 'OR')
        matches = [u for u in self.users if composite.matches(u)]
        self.assertEqual(len(matches), 2)

if __name__ == '__main__':
    unittest.main()