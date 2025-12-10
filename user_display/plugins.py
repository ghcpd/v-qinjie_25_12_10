# Simple plugin registry
_REGISTRY = {"filters": {}, "formatters": {}, "validators": {}}


def register(kind, name, obj):
    _REGISTRY[kind][name] = obj


def get(kind, name):
    return _REGISTRY.get(kind, {}).get(name)


def list_plugins(kind):
    return list(_REGISTRY.get(kind, {}).keys())

# register builtins
from .filters.regex_filter import RegexFilter
from .filters.composite_filter import CompositeFilter
from .formatters.compact import CompactFormatter
from .formatters.json_fmt import JsonFormatter
from .formatters.table import TableFormatter
from .validation.default import DefaultValidator

register('filters', 'regex', RegexFilter)
register('filters', 'composite', CompositeFilter)
register('formatters', 'compact', CompactFormatter)
register('formatters', 'json', JsonFormatter)
register('formatters', 'table', TableFormatter)
register('validators', 'default', DefaultValidator)