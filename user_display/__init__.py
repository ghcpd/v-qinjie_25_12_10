"""
user_display: High-performance, modular, concurrent user display system.

This package provides a comprehensive solution for managing and displaying user data
with support for multiple formatters, extensible filtering, field-level validation,
indexing, and optional snapshotting for MVCC-like concurrent reads.

Core modules:
    - store: Thread-safe user storage with indexing and snapshotting
    - formatters: Multiple output formats (JSON, compact, table)
    - filters: Extensible filtering strategies
    - validation: Field validation with soft-failure recovery
    - config: Centralized configuration system
    - logging_utils: Structured logging
    - metrics: Performance and usage metrics
    - plugins: Dynamic plugin registration system
"""

from .store import UserStore, UserSnapshot
from .formatters import (
    Formatter,
    FieldSelectingFormatter,
    JsonFormatter,
    CompactFormatter,
    TableFormatter,
)
from .filters import (
    Filter,
    LambdaFilter,
    CompositeFilter,
    RegexFilter,
    FieldMatchFilter,
    FieldContainsFilter,
    RangeFilter,
)
from .validation import (
    Validator,
    FieldValidator,
    CompositeValidator,
    EmailValidator,
    RoleValidator,
    StatusValidator,
    create_default_validator,
)
from .config import Config, get_config, reset_config
from .logging_utils import StructuredLogger, setup_logging, get_logger
from .metrics import Metrics, get_metrics, reset_metrics
from .plugins import PluginRegistry, get_plugin_registry, reset_plugin_registry
from .errors import (
    UserDisplayError,
    ValidationError,
    FormattingError,
    FilterError,
    StorageError,
    ConfigError,
    PluginError,
)

__version__ = "1.0.0"

__all__ = [
    # Store
    "UserStore",
    "UserSnapshot",
    # Formatters
    "Formatter",
    "FieldSelectingFormatter",
    "JsonFormatter",
    "CompactFormatter",
    "TableFormatter",
    # Filters
    "Filter",
    "LambdaFilter",
    "CompositeFilter",
    "RegexFilter",
    "FieldMatchFilter",
    "FieldContainsFilter",
    "RangeFilter",
    # Validation
    "Validator",
    "FieldValidator",
    "CompositeValidator",
    "EmailValidator",
    "RoleValidator",
    "StatusValidator",
    "create_default_validator",
    # Configuration
    "Config",
    "get_config",
    "reset_config",
    # Logging
    "StructuredLogger",
    "setup_logging",
    "get_logger",
    # Metrics
    "Metrics",
    "get_metrics",
    "reset_metrics",
    # Plugins
    "PluginRegistry",
    "get_plugin_registry",
    "reset_plugin_registry",
    # Errors
    "UserDisplayError",
    "ValidationError",
    "FormattingError",
    "FilterError",
    "StorageError",
    "ConfigError",
    "PluginError",
]
