"""
Tests for API compatibility with original module.
"""

import unittest
from user_display_original import display_users as orig_display, get_user_by_id as orig_get, filter_users as orig_filter, export_users_to_string as orig_export
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string

class TestAPICompatibility(unittest.TestCase):

    def setUp(self):
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin', 'status': 'Active', 'join_date': '2023-01-01', 'last_login': '2025-11-26'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User', 'status': 'Inactive', 'join_date': '2023-01-01', 'last_login': '2025-11-25'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'User', 'status': 'Active', 'join_date': '2023-01-01', 'last_login': '2025-11-24'},
        ]

    def test_display_users_basic(self):
        orig_result = orig_display(self.users.copy())
        opt_result = display_users(self.users.copy())

        # Should contain same user info (ignoring random elements from original)
        self.assertIn('ID=1', opt_result)
        self.assertIn('NAME=Alice', opt_result)
        self.assertIn('PROCESSED=3', opt_result)

    def test_get_user_by_id(self):
        orig_user = orig_get(self.users.copy(), 1)
        opt_user = get_user_by_id(self.users.copy(), 1)

        self.assertEqual(orig_user['id'], opt_user['id'])
        self.assertEqual(orig_user['name'], opt_user['name'])

        # Test missing ID
        self.assertIsNone(orig_get(self.users.copy(), 999))
        self.assertIsNone(get_user_by_id(self.users.copy(), 999))

    def test_filter_users(self):
        criteria = {'role': 'Admin'}
        orig_filtered = orig_filter(self.users.copy(), criteria)
        opt_filtered = filter_users(self.users.copy(), criteria)

        self.assertEqual(len(orig_filtered), len(opt_filtered))
        self.assertEqual(len(opt_filtered), 1)
        self.assertEqual(opt_filtered[0]['name'], 'Alice')

    def test_export_users(self):
        orig_exported = orig_export(self.users.copy())
        opt_exported = export_users_to_string(self.users.copy())

        # Should contain same structure
        self.assertIn('EXPORT_BEGIN', opt_exported)
        self.assertIn('EXPORT_END', opt_exported)
        self.assertIn('UserID: 1', opt_exported)
        self.assertIn('Name: Alice', opt_exported)

if __name__ == '__main__':
    unittest.main()