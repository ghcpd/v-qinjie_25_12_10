"""
Base formatter interface for user_display module.
Formatters provide different output formats for user data.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set


class Formatter(ABC):
    """
    Abstract base class for user formatters.
    Formatters convert user records to strings in various formats.
    """
    
    @abstractmethod
    def format(self, users: List[Dict[str, Any]], **options) -> str:
        """
        Format users to a string.
        
        Args:
            users: List of user dictionaries
            **options: Format-specific options
        
        Returns:
            Formatted string
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the formatter's name."""
        pass


class FieldSelectingFormatter(Formatter):
    """
    Base class for formatters that support field selection and conditional display.
    """
    
    def __init__(self, included_fields: Optional[Set[str]] = None,
                 excluded_fields: Optional[Set[str]] = None):
        """
        Initialize formatter.
        
        Args:
            included_fields: If set, only include these fields
            excluded_fields: If set, exclude these fields
        """
        self.included_fields = included_fields
        self.excluded_fields = excluded_fields or set()
    
    def should_include_field(self, field_name: str) -> bool:
        """Determine if a field should be included in output."""
        if field_name in self.excluded_fields:
            return False
        if self.included_fields is not None:
            return field_name in self.included_fields
        return True
    
    def filter_user_fields(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Filter a user record to include only selected fields."""
        return {
            k: v for k, v in user.items()
            if self.should_include_field(k)
        }
