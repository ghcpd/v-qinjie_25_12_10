"""
Error definitions for the user_display module.
Provides structured exception classes for validation, formatting, and filtering errors.
"""


class UserDisplayError(Exception):
    """Base exception for user_display module."""
    pass


class ValidationError(UserDisplayError):
    """Raised when user data fails validation."""
    pass


class FormattingError(UserDisplayError):
    """Raised when formatting fails."""
    pass


class FilterError(UserDisplayError):
    """Raised when filtering fails."""
    pass


class StorageError(UserDisplayError):
    """Raised when storage operations fail."""
    pass


class ConfigError(UserDisplayError):
    """Raised when configuration is invalid."""
    pass


class PluginError(UserDisplayError):
    """Raised when plugin registration or loading fails."""
    pass
