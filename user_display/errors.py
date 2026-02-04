"""
Custom exceptions for the user display system.
"""

class UserDisplayError(Exception):
    """Base exception for user display errors."""
    pass

class ValidationError(UserDisplayError):
    """Raised when user data validation fails."""
    pass

class FormatterError(UserDisplayError):
    """Raised when formatting fails."""
    pass

class FilterError(UserDisplayError):
    """Raised when filtering fails."""
    pass

class StoreError(UserDisplayError):
    """Raised when store operations fail."""
    pass