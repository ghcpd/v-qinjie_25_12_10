"""
Specialized filter implementations for user_display module.
"""

import re
from typing import List, Dict, Any, Optional, Pattern
from .base import Filter


class RegexFilter(Filter):
    """Filters users by regex match on a field."""
    
    def __init__(self, field_name: str, pattern: str, case_sensitive: bool = False):
        """
        Initialize regex filter.
        
        Args:
            field_name: Field to search
            pattern: Regex pattern
            case_sensitive: Whether to use case-sensitive matching
        """
        self.field_name = field_name
        self.pattern = pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            self.compiled_pattern: Pattern = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        self.case_sensitive = case_sensitive
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter users by regex match."""
        result = []
        for user in users:
            value = user.get(self.field_name)
            if value is not None:
                str_value = str(value)
                if self.compiled_pattern.search(str_value):
                    result.append(user)
        return result
    
    def get_name(self) -> str:
        return f"RegexFilter({self.field_name}, pattern={self.pattern})"


class FieldMatchFilter(Filter):
    """Filters users by exact field match."""
    
    def __init__(self, field_name: str, value: Any, case_sensitive: bool = True):
        """
        Initialize field match filter.
        
        Args:
            field_name: Field to match
            value: Value to match
            case_sensitive: For string values, whether to use case-sensitive matching
        """
        self.field_name = field_name
        self.value = value
        self.case_sensitive = case_sensitive
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter users by field value match."""
        result = []
        for user in users:
            field_value = user.get(self.field_name)
            
            if isinstance(self.value, str) and isinstance(field_value, str):
                if self.case_sensitive:
                    match = field_value == self.value
                else:
                    match = field_value.lower() == self.value.lower()
            else:
                match = field_value == self.value
            
            if match:
                result.append(user)
        
        return result
    
    def get_name(self) -> str:
        return f"FieldMatchFilter({self.field_name} == {self.value})"


class FieldContainsFilter(Filter):
    """Filters users by substring/contains match."""
    
    def __init__(self, field_name: str, substring: str, case_sensitive: bool = False):
        """
        Initialize field contains filter.
        
        Args:
            field_name: Field to search
            substring: Substring to find
            case_sensitive: Whether to use case-sensitive matching
        """
        self.field_name = field_name
        self.substring = substring
        self.case_sensitive = case_sensitive
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter users by substring match."""
        result = []
        for user in users:
            value = user.get(self.field_name)
            if value is not None:
                str_value = str(value)
                if self.case_sensitive:
                    match = self.substring in str_value
                else:
                    match = self.substring.lower() in str_value.lower()
                
                if match:
                    result.append(user)
        
        return result
    
    def get_name(self) -> str:
        return f"FieldContainsFilter({self.field_name} contains {self.substring})"


class RangeFilter(Filter):
    """Filters users by numeric range."""
    
    def __init__(self, field_name: str, min_value: Optional[float] = None,
                 max_value: Optional[float] = None):
        """
        Initialize range filter.
        
        Args:
            field_name: Field to compare
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
        """
        self.field_name = field_name
        self.min_value = min_value
        self.max_value = max_value
    
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter users by numeric range."""
        result = []
        for user in users:
            value = user.get(self.field_name)
            if value is not None:
                try:
                    numeric_value = float(value)
                    
                    in_range = True
                    if self.min_value is not None and numeric_value < self.min_value:
                        in_range = False
                    if self.max_value is not None and numeric_value > self.max_value:
                        in_range = False
                    
                    if in_range:
                        result.append(user)
                except (ValueError, TypeError):
                    pass
        
        return result
    
    def get_name(self) -> str:
        return f"RangeFilter({self.field_name}: {self.min_value}-{self.max_value})"
