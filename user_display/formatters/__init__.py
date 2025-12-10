"""
Formatters module for user_display.
Provides various output formats for user records.
"""

from .base import Formatter, FieldSelectingFormatter
from .json_fmt import JsonFormatter
from .compact import CompactFormatter
from .table import TableFormatter

__all__ = [
    "Formatter",
    "FieldSelectingFormatter",
    "JsonFormatter",
    "CompactFormatter",
    "TableFormatter",
]
