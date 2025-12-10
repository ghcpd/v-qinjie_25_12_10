"""
Default validator implementations for user_display module.
Provides standard validation rules for user records.
"""

from typing import Any, Dict, List, Tuple
import re
from .base import Validator, CompositeValidator, FieldValidator


class EmailValidator(Validator):
    """Validates email field format."""
    
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate email format if present."""
        issues = []
        email = user.get("email")
        
        if email is not None and isinstance(email, str):
            # Simple email regex
            if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
                issues.append(f"Invalid email format: {email}")
        
        return len(issues) == 0, issues
    
    def get_name(self) -> str:
        return "EmailValidator"


class RoleValidator(Validator):
    """Validates role field has allowed values."""
    
    def __init__(self, allowed_roles: List[str]):
        """Initialize with allowed roles."""
        self.allowed_roles = allowed_roles
    
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate role is in allowed list."""
        issues = []
        role = user.get("role")
        
        if role is not None and role not in self.allowed_roles:
            issues.append(f"Role '{role}' not in allowed list: {self.allowed_roles}")
        
        return len(issues) == 0, issues
    
    def get_name(self) -> str:
        return "RoleValidator"


class StatusValidator(Validator):
    """Validates status field has allowed values."""
    
    def __init__(self, allowed_statuses: List[str]):
        """Initialize with allowed statuses."""
        self.allowed_statuses = allowed_statuses
    
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate status is in allowed list."""
        issues = []
        status = user.get("status")
        
        if status is not None and status not in self.allowed_statuses:
            issues.append(f"Status '{status}' not in allowed list: {self.allowed_statuses}")
        
        return len(issues) == 0, issues
    
    def get_name(self) -> str:
        return "StatusValidator"


def create_default_validator() -> CompositeValidator:
    """Create a default validator with standard rules."""
    composite = CompositeValidator()
    
    # Required fields: id, name
    composite.add_validator(FieldValidator(
        required_fields=["id"],
        field_types={}
    ))
    
    # Email validation
    composite.add_validator(EmailValidator())
    
    # Role validation
    composite.add_validator(RoleValidator(["Admin", "User", "Mod"]))
    
    # Status validation
    composite.add_validator(StatusValidator(["Active", "Inactive"]))
    
    return composite
