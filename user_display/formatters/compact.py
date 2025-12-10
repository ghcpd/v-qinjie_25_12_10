"""
Compact formatter for user_display module.
Outputs users in a compact pipe-delimited format.
"""

from typing import List, Dict, Any, Optional, Set
from .base import FieldSelectingFormatter


class CompactFormatter(FieldSelectingFormatter):
    """Formats users in a compact pipe-delimited format."""
    
    def __init__(self, included_fields: Optional[Set[str]] = None,
                 excluded_fields: Optional[Set[str]] = None,
                 separator: str = " | ",
                 include_header: bool = True,
                 max_field_length: Optional[int] = None):
        """
        Initialize compact formatter.
        
        Args:
            included_fields: If set, only include these fields
            excluded_fields: If set, exclude these fields
            separator: Separator between fields
            include_header: Whether to include header row
            max_field_length: Maximum length for field values (None = no limit)
        """
        super().__init__(included_fields, excluded_fields)
        self.separator = separator
        self.include_header = include_header
        self.max_field_length = max_field_length
    
    def _truncate_field(self, value: str) -> str:
        """Truncate a field value if needed."""
        if self.max_field_length and len(value) > self.max_field_length:
            return value[:self.max_field_length - 3] + "..."
        return value
    
    def format(self, users: List[Dict[str, Any]], **options) -> str:
        """Format users in compact format."""
        if not users:
            return ""
        
        lines = []
        
        # Get all possible field names from first user
        all_fields = set()
        for user in users:
            all_fields.update(user.keys())
        
        # Filter to included/excluded fields
        selected_fields = [f for f in sorted(all_fields) if self.should_include_field(f)]
        
        # Header
        if self.include_header and selected_fields:
            header = self.separator.join(selected_fields)
            lines.append(header)
        
        # Data rows
        for user in users:
            values = []
            for field in selected_fields:
                value = str(user.get(field, ""))
                value = self._truncate_field(value)
                values.append(value)
            lines.append(self.separator.join(values))
        
        return "\n".join(lines)
    
    def get_name(self) -> str:
        return "CompactFormatter"
