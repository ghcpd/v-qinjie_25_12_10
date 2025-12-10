"""
Structured logging and debug utilities for user_display module.
Provides hierarchical logging with configurable levels and formatters.
"""

import logging
import json
from typing import Any, Dict, Optional
from datetime import datetime
from enum import Enum

from .config import get_config


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class StructuredLogger:
    """
    Structured logging that outputs JSON or plain text.
    Supports context injection and hierarchical logging.
    """
    
    def __init__(self, name: str):
        """Initialize logger with a name."""
        self.name = name
        self.logger = logging.getLogger(f"user_display.{name}")
        self._context: Dict[str, Any] = {}
    
    def set_context(self, key: str, value: Any) -> None:
        """Set a context variable to be included in all logs."""
        self._context[key] = value
    
    def update_context(self, updates: Dict[str, Any]) -> None:
        """Update multiple context variables."""
        self._context.update(updates)
    
    def clear_context(self) -> None:
        """Clear all context variables."""
        self._context.clear()
    
    def _format_message(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """Format a log message as structured data."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "logger": self.name,
            "level": level,
            "message": message,
            **self._context,
            **kwargs
        }
        return log_entry
    
    def debug(self, message: str, **kwargs) -> None:
        """Log a debug message."""
        entry = self._format_message("DEBUG", message, **kwargs)
        self.logger.debug(json.dumps(entry))
    
    def info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        entry = self._format_message("INFO", message, **kwargs)
        self.logger.info(json.dumps(entry))
    
    def warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        entry = self._format_message("WARNING", message, **kwargs)
        self.logger.warning(json.dumps(entry))
    
    def error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        entry = self._format_message("ERROR", message, **kwargs)
        self.logger.error(json.dumps(entry))
    
    def critical(self, message: str, **kwargs) -> None:
        """Log a critical message."""
        entry = self._format_message("CRITICAL", message, **kwargs)
        self.logger.critical(json.dumps(entry))


def setup_logging(level: Optional[str] = None) -> None:
    """
    Set up basic logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    if level is None:
        config = get_config()
        level = config.get("log_level", "INFO")
    
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_logger(name: str) -> StructuredLogger:
    """Get or create a structured logger for the given name."""
    return StructuredLogger(name)
