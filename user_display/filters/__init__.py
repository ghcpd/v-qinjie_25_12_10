"""
Filters module for user_display.
Provides extensible filtering strategies.
"""

from .base import Filter, LambdaFilter, CompositeFilter
from .regex_filter import (
    RegexFilter,
    FieldMatchFilter,
    FieldContainsFilter,
    RangeFilter,
)

__all__ = [
    "Filter",
    "LambdaFilter",
    "CompositeFilter",
    "RegexFilter",
    "FieldMatchFilter",
    "FieldContainsFilter",
    "RangeFilter",
]
