"""
Base validator interface and abstract classes for user_display module.
Validators handle field-level validation with soft-failure recovery.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Optional


class Validator(ABC):
    """
    Abstract base class for validators.
    Validators check individual fields and provide recovery suggestions.
    """
    
    @abstractmethod
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a user record.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the validator's name."""
        pass


class FieldValidator(Validator):
    """Validates individual fields based on type and presence rules."""
    
    def __init__(self, required_fields: Optional[List[str]] = None,
                 field_types: Optional[Dict[str, type]] = None):
        """
        Initialize field validator.
        
        Args:
            required_fields: List of field names that must be present
            field_types: Dictionary mapping field names to expected types
        """
        self.required_fields = required_fields or []
        self.field_types = field_types or {}
    
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate field presence and types."""
        issues = []
        
        # Check required fields
        for field in self.required_fields:
            if field not in user or user[field] is None:
                issues.append(f"Missing required field: {field}")
        
        # Check field types
        for field, expected_type in self.field_types.items():
            if field in user and user[field] is not None:
                if not isinstance(user[field], expected_type):
                    issues.append(f"Field '{field}' has incorrect type (expected {expected_type.__name__})")
        
        return len(issues) == 0, issues
    
    def get_name(self) -> str:
        """Get the validator's name."""
        return "FieldValidator"


class CompositeValidator(Validator):
    """Combines multiple validators."""
    
    def __init__(self, validators: Optional[List[Validator]] = None):
        """Initialize with a list of validators."""
        self.validators = validators or []
    
    def add_validator(self, validator: Validator) -> None:
        """Add a validator to the composite."""
        self.validators.append(validator)
    
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Run all validators and collect issues."""
        all_issues = []
        for validator in self.validators:
            is_valid, issues = validator.validate(user)
            all_issues.extend(issues)
        
        return len(all_issues) == 0, all_issues
    
    def get_name(self) -> str:
        """Get the validator's name."""
        return "CompositeValidator"
