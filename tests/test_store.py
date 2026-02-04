"""
Tests for UserStore.
"""

import unittest
from user_display.store import UserStore

class TestUserStore(unittest.TestCase):

    def setUp(self):
        self.store = UserStore()
        self.users = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'User'},
        ]

    def test_add_and_get(self):
        self.store.add_users(self.users)
        user = self.store.get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], 'Alice')

    def test_get_missing(self):
        self.store.add_users(self.users)
        user = self.store.get_user_by_id(999)
        self.assertIsNone(user)

    def test_filter(self):
        self.store.add_users(self.users)
        admins = self.store.filter_users(lambda u: u.get('role') == 'Admin')
        self.assertEqual(len(admins), 1)

    def test_snapshot(self):
        self.store.add_users(self.users)
        self.store.create_snapshot('test')
        self.assertEqual(len(self.store.get_all_users()), 2)

        # Modify
        self.store.add_users([{'id': 3, 'name': 'Charlie'}])
        self.assertEqual(len(self.store.get_all_users()), 3)

        # Load snapshot
        self.store.load_snapshot('test')
        self.assertEqual(len(self.store.get_all_users()), 2)

if __name__ == '__main__':
    unittest.main()