"""
Regex-based filter.
"""

import re
from typing import Dict, Any
from .base import BaseFilter

class RegexFilter(BaseFilter):
    """Filter using regex patterns."""

    def __init__(self, criteria: Dict[str, Any], case_sensitive: bool = False):
        super().__init__(criteria, case_sensitive)
        self._compiled_patterns = {}
        for key, pattern in criteria.items():
            flags = 0 if case_sensitive else re.IGNORECASE
            try:
                self._compiled_patterns[key] = re.compile(pattern, flags)
            except re.error as e:
                raise ValueError(f"Invalid regex for {key}: {pattern}") from e

    def _value_matches(self, actual: Any, expected: Any, key: str = None) -> bool:
        """Check if actual matches the regex pattern."""
        pattern = self._compiled_patterns[key]
        actual_str = str(actual)
        return bool(pattern.search(actual_str))