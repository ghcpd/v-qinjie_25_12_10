"""
Plugin system for user_display module.
Allows dynamic registration of filters, formatters, and validators.
"""

from typing import Dict, Any, Type, Optional, List
from .filters import Filter
from .formatters import Formatter
from .validation import Validator
from .errors import PluginError
from .logging_utils import get_logger


logger = get_logger("plugins")


class PluginRegistry:
    """
    Central registry for plugins (filters, formatters, validators).
    Supports dynamic registration and lookup.
    """
    
    def __init__(self):
        """Initialize plugin registry."""
        self._filters: Dict[str, Type[Filter]] = {}
        self._formatters: Dict[str, Type[Formatter]] = {}
        self._validators: Dict[str, Type[Validator]] = {}
    
    def register_filter(self, name: str, filter_class: Type[Filter]) -> None:
        """Register a filter class."""
        if not issubclass(filter_class, Filter):
            raise PluginError(f"Filter class must inherit from Filter: {filter_class}")
        self._filters[name] = filter_class
        logger.info("Filter registered", name=name, class_name=filter_class.__name__)
    
    def register_formatter(self, name: str, formatter_class: Type[Formatter]) -> None:
        """Register a formatter class."""
        if not issubclass(formatter_class, Formatter):
            raise PluginError(f"Formatter class must inherit from Formatter: {formatter_class}")
        self._formatters[name] = formatter_class
        logger.info("Formatter registered", name=name, class_name=formatter_class.__name__)
    
    def register_validator(self, name: str, validator_class: Type[Validator]) -> None:
        """Register a validator class."""
        if not issubclass(validator_class, Validator):
            raise PluginError(f"Validator class must inherit from Validator: {validator_class}")
        self._validators[name] = validator_class
        logger.info("Validator registered", name=name, class_name=validator_class.__name__)
    
    def get_filter(self, name: str) -> Optional[Type[Filter]]:
        """Get a registered filter class."""
        return self._filters.get(name)
    
    def get_formatter(self, name: str) -> Optional[Type[Formatter]]:
        """Get a registered formatter class."""
        return self._formatters.get(name)
    
    def get_validator(self, name: str) -> Optional[Type[Validator]]:
        """Get a registered validator class."""
        return self._validators.get(name)
    
    def list_filters(self) -> List[str]:
        """List all registered filter names."""
        return list(self._filters.keys())
    
    def list_formatters(self) -> List[str]:
        """List all registered formatter names."""
        return list(self._formatters.keys())
    
    def list_validators(self) -> List[str]:
        """List all registered validator names."""
        return list(self._validators.keys())
    
    def unregister_filter(self, name: str) -> None:
        """Unregister a filter."""
        if name in self._filters:
            del self._filters[name]
            logger.info("Filter unregistered", name=name)
    
    def unregister_formatter(self, name: str) -> None:
        """Unregister a formatter."""
        if name in self._formatters:
            del self._formatters[name]
            logger.info("Formatter unregistered", name=name)
    
    def unregister_validator(self, name: str) -> None:
        """Unregister a validator."""
        if name in self._validators:
            del self._validators[name]
            logger.info("Validator unregistered", name=name)


# Global plugin registry
_global_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """Get or create the global plugin registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PluginRegistry()
        _register_default_plugins()
    return _global_registry


def _register_default_plugins() -> None:
    """Register default plugins."""
    registry = _global_registry
    
    # Formatters
    from .formatters import JsonFormatter, CompactFormatter, TableFormatter
    registry.register_formatter("json", JsonFormatter)
    registry.register_formatter("compact", CompactFormatter)
    registry.register_formatter("table", TableFormatter)
    
    # Filters
    from .filters import LambdaFilter, CompositeFilter, RegexFilter, FieldMatchFilter, FieldContainsFilter, RangeFilter
    registry.register_filter("lambda", LambdaFilter)
    registry.register_filter("composite", CompositeFilter)
    registry.register_filter("regex", RegexFilter)
    registry.register_filter("field_match", FieldMatchFilter)
    registry.register_filter("field_contains", FieldContainsFilter)
    registry.register_filter("range", RangeFilter)


def reset_plugin_registry() -> None:
    """Reset the global plugin registry."""
    global _global_registry
    _global_registry = None
