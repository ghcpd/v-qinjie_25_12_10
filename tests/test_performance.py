"""
Performance tests.
"""

import unittest
import time
from user_display_optimized import display_users, filter_users, get_user_by_id, export_users_to_string

class TestPerformance(unittest.TestCase):

    def setUp(self):
        # Generate 50,000 users
        self.users = [
            {
                'id': i,
                'name': f'User{i}',
                'email': f'user{i}@example.com',
                'role': 'Admin' if i % 100 == 0 else 'User',
                'status': 'Active' if i % 2 == 0 else 'Inactive',
                'join_date': '2023-01-01',
                'last_login': '2025-11-26'
            }
            for i in range(1, 50001)
        ]

    def test_display_performance(self):
        start = time.time()
        result = display_users(self.users, show_all=False)
        duration = time.time() - start
        self.assertLess(duration, 1.0, f"Display took {duration:.3f}s, target <1.0s")
        self.assertIn('ID=1', result)

    def test_filter_performance(self):
        start = time.time()
        filtered = filter_users(self.users, {'role': 'Admin'})
        duration = time.time() - start
        self.assertLess(duration, 5.0, f"Filter took {duration:.3f}s, target <5.0s")
        self.assertGreater(len(filtered), 400)  # ~500 admins

    def test_id_lookup_performance(self):
        # Warm up
        get_user_by_id(self.users, 1)

        start = time.time()
        user = get_user_by_id(self.users, 25000)
        duration = time.time() - start
        self.assertLess(duration, 0.001, f"Lookup took {duration:.6f}s, target <0.001s")
        self.assertEqual(user['id'], 25000)

    def test_export_performance(self):
        start = time.time()
        exported = export_users_to_string(self.users)
        duration = time.time() - start
        # Export target not specified, but should be reasonable
        self.assertLess(duration, 2.0, f"Export took {duration:.3f}s")
        self.assertIn('EXPORT_BEGIN', exported)

if __name__ == '__main__':
    unittest.main()