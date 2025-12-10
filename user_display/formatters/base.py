"""
Base formatter classes.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..errors import FormatterError
from ..logging_utils import logger

class Formatter(ABC):
    """Abstract base class for formatters."""

    @abstractmethod
    def format_users(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format a list of users to string."""
        pass

    @abstractmethod
    def format_user(self, user: Dict[str, Any], **kwargs) -> str:
        """Format a single user to string."""
        pass

class BaseFormatter(Formatter):
    """Base formatter with common functionality."""

    def __init__(self, fields: List[str] = None, separator: str = ' | '):
        self.fields = fields or ['id', 'name', 'email', 'role', 'status', 'join_date', 'last_login']
        self.separator = separator

    def format_users(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format multiple users."""
        lines = []
        for user in users:
            lines.append(self.format_user(user, **kwargs))
        return '\n'.join(lines)

    def format_user(self, user: Dict[str, Any], **kwargs) -> str:
        """Format a single user."""
        parts = []
        for field in self.fields:
            value = user.get(field, 'N/A')
            parts.append(f"{field.upper()}={value}")
        return self.separator.join(parts)

class TableFormatter(BaseFormatter):
    """Table-style formatter."""

    def format_users(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format as a table."""
        if not users:
            return "No users"

        lines = []
        # Header
        header = self.separator.join(f.upper() for f in self.fields)
        lines.append(header)
        lines.append('-' * len(header))

        # Rows
        for user in users:
            row = []
            for field in self.fields:
                value = str(user.get(field, 'N/A'))
                row.append(value)
            lines.append(self.separator.join(row))

        return '\n'.join(lines)