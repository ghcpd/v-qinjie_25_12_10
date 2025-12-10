"""
JSON formatter.
"""

import json
from typing import Dict, Any, List
from .base import Formatter

class JSONFormatter(Formatter):
    """JSON formatter."""

    def format_users(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format users as JSON array."""
        indent = kwargs.get('indent', 2)
        return json.dumps(users, indent=indent)

    def format_user(self, user: Dict[str, Any], **kwargs) -> str:
        """Format single user as JSON."""
        indent = kwargs.get('indent', 2)
        return json.dumps(user, indent=indent)