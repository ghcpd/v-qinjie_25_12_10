"""
Base filter classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable
from ..errors import FilterError
from ..logging_utils import logger

class Filter(ABC):
    """Abstract base class for filters."""

    @abstractmethod
    def matches(self, user: Dict[str, Any]) -> bool:
        """Return True if user matches the filter criteria."""
        pass

class BaseFilter(Filter):
    """Base filter with common functionality."""

    def __init__(self, criteria: Dict[str, Any], case_sensitive: bool = False):
        self.criteria = criteria
        self.case_sensitive = case_sensitive

    def _normalize_value(self, value: Any) -> str:
        """Normalize value for comparison."""
        if not isinstance(value, str):
            value = str(value)
        return value if self.case_sensitive else value.lower()

    def matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all criteria."""
        for key, expected in self.criteria.items():
            actual = user.get(key)
            if actual is None:
                return False
            if not self._value_matches(actual, expected, key):
                return False
        return True

    def _value_matches(self, actual: Any, expected: Any, key: str = None) -> bool:
        """Check if actual value matches expected."""
        actual_norm = self._normalize_value(actual)
        expected_norm = self._normalize_value(expected)
        return actual_norm == expected_norm

class CompositeFilter(Filter):
    """Filter that combines multiple filters with AND/OR logic."""

    def __init__(self, filters: List[Filter], operator: str = 'AND'):
        self.filters = filters
        self.operator = operator.upper()
        if self.operator not in ['AND', 'OR']:
            raise FilterError(f"Invalid operator: {operator}")

    def matches(self, user: Dict[str, Any]) -> bool:
        if self.operator == 'AND':
            return all(f.matches(user) for f in self.filters)
        else:  # OR
            return any(f.matches(user) for f in self.filters)