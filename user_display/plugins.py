"""
Plugin system for dynamic registration of filters, formatters, and validators.
"""

from typing import Dict, Type, Any
from .logging_utils import logger

class PluginRegistry:
    """Registry for plugins."""

    def __init__(self):
        self._plugins: Dict[str, Dict[str, Type]] = {
            'formatters': {},
            'filters': {},
            'validators': {},
        }

    def register_formatter(self, name: str, cls: Type):
        """Register a formatter class."""
        self._plugins['formatters'][name] = cls
        logger.info(f"Registered formatter: {name}")

    def register_filter(self, name: str, cls: Type):
        """Register a filter class."""
        self._plugins['filters'][name] = cls
        logger.info(f"Registered filter: {name}")

    def register_validator(self, name: str, cls: Type):
        """Register a validator class."""
        self._plugins['validators'][name] = cls
        logger.info(f"Registered validator: {name}")

    def get_formatter(self, name: str) -> Type:
        """Get a formatter class by name."""
        return self._plugins['formatters'].get(name)

    def get_filter(self, name: str) -> Type:
        """Get a filter class by name."""
        return self._plugins['filters'].get(name)

    def get_validator(self, name: str) -> Type:
        """Get a validator class by name."""
        return self._plugins['validators'].get(name)

    def list_formatters(self) -> list:
        """List registered formatter names."""
        return list(self._plugins['formatters'].keys())

    def list_filters(self) -> list:
        """List registered filter names."""
        return list(self._plugins['filters'].keys())

    def list_validators(self) -> list:
        """List registered validator names."""
        return list(self._plugins['validators'].keys())

# Global registry instance
registry = PluginRegistry()