"""
Base validator classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..errors import ValidationError
from ..logging_utils import logger

class Validator(ABC):
    """Abstract base class for validators."""

    @abstractmethod
    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and potentially repair a user dict. Raise ValidationError if unrecoverable."""
        pass

    @abstractmethod
    def get_required_fields(self) -> List[str]:
        """Return list of required fields."""
        pass

class BaseValidator(Validator):
    """Base validator with common functionality."""

    def __init__(self, required_fields: List[str] = None, strict: bool = False):
        self.required_fields = required_fields or ['id', 'name', 'email']
        self.strict = strict

    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Basic validation: check required fields, fill defaults."""
        if not isinstance(user, dict):
            if self.strict:
                raise ValidationError("User must be a dict")
            logger.warning("User is not a dict, creating empty", user_type=type(user))
            user = {}

        validated = user.copy()

        for field in self.required_fields:
            if field not in validated or validated[field] is None:
                if self.strict:
                    raise ValidationError(f"Missing required field: {field}")
                # Fill defaults
                if field == 'id':
                    validated[field] = -1
                elif field in ['name', 'email']:
                    validated[field] = 'Unknown'
                else:
                    validated[field] = ''

        # Ensure id is int
        if 'id' in validated:
            try:
                validated['id'] = int(validated['id'])
            except (ValueError, TypeError):
                if self.strict:
                    raise ValidationError("ID must be convertible to int")
                validated['id'] = -1

        return validated

    def get_required_fields(self) -> List[str]:
        return self.required_fields