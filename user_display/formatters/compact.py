"""
Compact formatter.
"""

from typing import Dict, Any, List
from .base import BaseFormatter

class CompactFormatter(BaseFormatter):
    """Compact formatter with minimal output."""

    def __init__(self, fields: List[str] = None):
        super().__init__(fields or ['id', 'name'], separator=' ')

    def format_user(self, user: Dict[str, Any], **kwargs) -> str:
        """Format user compactly."""
        return f"{user.get('id', 'N/A')}: {user.get('name', 'Unknown')}"