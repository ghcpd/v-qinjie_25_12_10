"""
Table formatter for user_display module.
Outputs users in an ASCII table format.
"""

from typing import List, Dict, Any, Optional, Set
from .base import FieldSelectingFormatter


class TableFormatter(FieldSelectingFormatter):
    """Formats users as an ASCII table."""
    
    def __init__(self, included_fields: Optional[Set[str]] = None,
                 excluded_fields: Optional[Set[str]] = None,
                 border_char: str = "=",
                 max_field_length: Optional[int] = 30):
        """
        Initialize table formatter.
        
        Args:
            included_fields: If set, only include these fields
            excluded_fields: If set, exclude these fields
            border_char: Character to use for borders
            max_field_length: Maximum column width
        """
        super().__init__(included_fields, excluded_fields)
        self.border_char = border_char
        self.max_field_length = max_field_length
    
    def _truncate_field(self, value: str, max_len: int) -> str:
        """Truncate a field value to max length."""
        if len(value) > max_len:
            return value[:max_len - 3] + "..."
        return value
    
    def format(self, users: List[Dict[str, Any]], **options) -> str:
        """Format users as a table."""
        if not users:
            return ""
        
        # Get selected fields
        all_fields = set()
        for user in users:
            all_fields.update(user.keys())
        
        fields = [f for f in sorted(all_fields) if self.should_include_field(f)]
        if not fields:
            return ""
        
        # Calculate column widths
        col_widths = {}
        for field in fields:
            max_width = len(field)
            for user in users:
                value_len = len(str(user.get(field, "")))
                max_width = max(max_width, value_len)
            
            if self.max_field_length:
                max_width = min(max_width, self.max_field_length)
            col_widths[field] = max_width
        
        # Build table
        lines = []
        
        # Top border
        total_width = sum(col_widths.values()) + (len(fields) - 1) * 3 + 4
        lines.append(self.border_char * total_width)
        
        # Header
        header_parts = []
        for field in fields:
            header_parts.append(field.ljust(col_widths[field]))
        lines.append("| " + " | ".join(header_parts) + " |")
        
        # Header border
        lines.append(self.border_char * total_width)
        
        # Data rows
        for user in users:
            row_parts = []
            for field in fields:
                value = str(user.get(field, ""))
                value = self._truncate_field(value, col_widths[field])
                row_parts.append(value.ljust(col_widths[field]))
            lines.append("| " + " | ".join(row_parts) + " |")
        
        # Bottom border
        lines.append(self.border_char * total_width)
        
        return "\n".join(lines)
    
    def get_name(self) -> str:
        return "TableFormatter"
