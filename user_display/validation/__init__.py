"""
Validation module for user_display.
Provides field-level validation with soft-failure recovery.
"""

from .base import Validator, FieldValidator, CompositeValidator
from .default import (
    EmailValidator,
    RoleValidator,
    StatusValidator,
    create_default_validator,
)

__all__ = [
    "Validator",
    "FieldValidator",
    "CompositeValidator",
    "EmailValidator",
    "RoleValidator",
    "StatusValidator",
    "create_default_validator",
]
