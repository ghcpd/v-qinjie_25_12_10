"""
Tests for validation.
"""

import unittest
from user_display.validation import DefaultValidator
from user_display.errors import ValidationError

class TestValidation(unittest.TestCase):

    def setUp(self):
        self.validator = DefaultValidator()

    def test_valid_user(self):
        user = {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'Admin', 'status': 'Active'}
        validated = self.validator.validate(user)
        self.assertEqual(validated['id'], 1)
        self.assertEqual(validated['name'], 'Alice')

    def test_missing_fields_strict(self):
        validator = DefaultValidator(strict=True)
        user = {'id': 1, 'name': 'Alice'}  # Missing email
        with self.assertRaises(ValidationError):
            validator.validate(user)

    def test_missing_fields_fallback(self):
        user = {'id': 1, 'name': 'Alice'}  # Missing email, role, status
        validated = self.validator.validate(user)
        self.assertEqual(validated['email'], 'Unknown')
        self.assertEqual(validated['role'], '')
        self.assertEqual(validated['status'], '')

    def test_invalid_id(self):
        user = {'id': 'invalid', 'name': 'Alice', 'email': 'alice@example.com'}
        validated = self.validator.validate(user)
        self.assertEqual(validated['id'], -1)  # Fallback

    def test_invalid_id_strict(self):
        validator = DefaultValidator(strict=True)
        user = {'id': 'invalid', 'name': 'Alice', 'email': 'alice@example.com'}
        with self.assertRaises(ValidationError):
            validator.validate(user)

if __name__ == '__main__':
    unittest.main()