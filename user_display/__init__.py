"""
User Display Package.
"""

from .store import UserStore
from .index import UserIndex
from .formatters import BaseFormatter, CompactFormatter, JSONFormatter, TableFormatter
from .filters import BaseFilter, RegexFilter, CompositeFilter
from .validation import DefaultValidator
from .config import config
from .logging_utils import logger
from .metrics import metrics
from .plugins import registry
from .errors import UserDisplayError, ValidationError, FormatterError, FilterError, StoreError

# Register built-in plugins
registry.register_formatter('default', BaseFormatter)
registry.register_formatter('compact', CompactFormatter)
registry.register_formatter('json', JSONFormatter)
registry.register_formatter('table', TableFormatter)

registry.register_filter('exact', BaseFilter)
registry.register_filter('regex', RegexFilter)
registry.register_filter('composite', CompositeFilter)

registry.register_validator('default', DefaultValidator)

__all__ = [
    'UserStore', 'UserIndex',
    'BaseFormatter', 'CompactFormatter', 'JSONFormatter', 'TableFormatter',
    'BaseFilter', 'RegexFilter', 'CompositeFilter',
    'DefaultValidator',
    'config', 'logger', 'metrics', 'registry',
    'UserDisplayError', 'ValidationError', 'FormatterError', 'FilterError', 'StoreError'
]