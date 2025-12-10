"""
Logging utilities for structured logging.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
from .config import config

class StructuredLogger:
    """Logger that outputs structured JSON logs."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.get('log_level', 'INFO')))
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _log(self, level: int, message: str, **kwargs):
        """Log a structured message."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': logging.getLevelName(level),
            'message': message,
            **kwargs
        }
        self.logger.log(level, json.dumps(log_entry))

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        self._log(logging.CRITICAL, message, **kwargs)

# Global logger instance
logger = StructuredLogger('user_display')