from .base import Formatter
from .compact import CompactFormatter
from .json_fmt import JSONFormatter
from .table import TableFormatter

class Registry:
    _registry = {
        "compact": CompactFormatter(),
        "json": JSONFormatter(),
        "table": TableFormatter(),
    }

    @classmethod
    def resolve(cls, key):
        if isinstance(key, Formatter):
            return key
        if callable(key):
            return key
        return cls._registry.get(str(key), CompactFormatter())
