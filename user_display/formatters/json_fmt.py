"""
JSON formatter for user_display module.
Outputs user records as formatted JSON.
"""

import json
from typing import List, Dict, Any, Optional, Set
from .base import FieldSelectingFormatter


class JsonFormatter(FieldSelectingFormatter):
    """Formats users as JSON."""
    
    def __init__(self, included_fields: Optional[Set[str]] = None,
                 excluded_fields: Optional[Set[str]] = None,
                 indent: Optional[int] = 2,
                 sort_keys: bool = False):
        """
        Initialize JSON formatter.
        
        Args:
            included_fields: If set, only include these fields
            excluded_fields: If set, exclude these fields
            indent: JSON indentation level (None for compact)
            sort_keys: Whether to sort keys
        """
        super().__init__(included_fields, excluded_fields)
        self.indent = indent
        self.sort_keys = sort_keys
    
    def format(self, users: List[Dict[str, Any]], **options) -> str:
        """Format users as JSON."""
        filtered_users = [self.filter_user_fields(u) for u in users]
        
        return json.dumps(
            filtered_users,
            indent=self.indent,
            sort_keys=self.sort_keys,
            default=str
        )
    
    def filter_user_fields(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Filter user fields based on included/excluded settings."""
        return {k: v for k, v in user.items() if self.should_include_field(k)}
    
    def get_name(self) -> str:
        return "JsonFormatter"
