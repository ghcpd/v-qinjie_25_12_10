#!/usr/bin/env python
"""
Fast test runner for user_display module.
Runs functional tests quickly, skips heavy performance tests.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_display import (
    UserStore,
    JsonFormatter,
    CompactFormatter,
    TableFormatter,
    RegexFilter,
    FieldMatchFilter,
    FieldContainsFilter,
    CompositeFilter,
    create_default_validator,
    EmailValidator,
    StatusValidator,
    get_config,
    get_metrics,
    reset_metrics,
    get_logger,
    setup_logging,
)
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
    reset_store,
)


class TestQuick(unittest.TestCase):
    """Quick smoke tests for core functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        reset_store()
        reset_metrics()
        self.users = [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin", "status": "Active"},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "User", "status": "Inactive"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "User", "status": "Active"},
        ]
    
    def test_formatters_work(self):
        """Test all formatters produce output."""
        formatters = [
            CompactFormatter(),
            JsonFormatter(),
            TableFormatter(),
        ]
        
        for fmt in formatters:
            output = fmt.format(self.users)
            self.assertTrue(len(output) > 0, f"{fmt.get_name()} produced empty output")
    
    def test_filters_work(self):
        """Test basic filtering."""
        # Exact match filter
        f = FieldMatchFilter("role", "Admin")
        result = f.apply(self.users)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Alice")
        
        # Contains filter
        f = FieldContainsFilter("name", "li")
        result = f.apply(self.users)
        self.assertEqual(len(result), 2)  # Alice and Charlie
    
    def test_store_operations(self):
        """Test store basic operations."""
        store = UserStore()
        
        for user in self.users:
            store.add_user(user, validate=False)
        
        # Test size
        self.assertEqual(store.size(), 3)
        
        # Test O(1) lookup
        user = store.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Alice")
        
        # Test missing lookup
        user = store.get_user(999)
        self.assertIsNone(user)
    
    def test_validation_works(self):
        """Test validation with issues."""
        validator = create_default_validator()
        
        # Valid user
        is_valid, issues = validator.validate(self.users[0])
        # May have issues but shouldn't crash
        self.assertIsInstance(is_valid, bool)
        self.assertIsInstance(issues, list)
    
    def test_api_display_users(self):
        """Test display_users API."""
        result = display_users(self.users)
        self.assertIn("Alice", result)
        self.assertIn("Bob", result)
        self.assertIn("PROCESSED=3", result)
    
    def test_api_get_user_by_id(self):
        """Test get_user_by_id API."""
        user = get_user_by_id(self.users, 1)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Alice")
    
    def test_api_filter_users(self):
        """Test filter_users API."""
        result = filter_users(self.users, {"name": "Alice"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Alice")
    
    def test_api_export_users(self):
        """Test export_users_to_string API."""
        result = export_users_to_string(self.users)
        self.assertIn("EXPORT_BEGIN", result)
        self.assertIn("EXPORT_END", result)
        self.assertIn("Alice", result)
    
    def test_performance_100_users(self):
        """Quick performance test with 100 users."""
        import time
        
        users = [
            {"id": i, "name": f"User{i}", "email": f"u{i}@test.com", "role": "User", "status": "Active"}
            for i in range(100)
        ]
        
        start = time.time()
        display_users(users)
        duration_ms = (time.time() - start) * 1000
        
        # Should complete in reasonable time (first call slower due to imports)
        self.assertLess(duration_ms, 500, f"display_users(100) took {duration_ms}ms")


if __name__ == "__main__":
    setup_logging("INFO")
    
    print("=" * 80)
    print("User Display - Quick Test Suite")
    print("=" * 80)
    print()
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestQuick)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print metrics
    print("\n" + "=" * 80)
    print("Metrics:")
    print(get_metrics())
    print("=" * 80)
    
    sys.exit(0 if result.wasSuccessful() else 1)
