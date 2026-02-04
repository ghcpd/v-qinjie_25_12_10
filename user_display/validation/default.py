"""
Default validator implementation.
"""

from typing import Dict, Any, List
from .base import BaseValidator

class DefaultValidator(BaseValidator):
    """Default validator with standard field requirements."""

    def __init__(self, strict: bool = False):
        super().__init__(required_fields=['id', 'name', 'email', 'role', 'status'], strict=strict)