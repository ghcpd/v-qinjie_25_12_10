from .base import BaseFilter
from .regex_filter import RegexFilter
from .composite_filter import CompositeFilter

class Registry:
    _registry = {
        "regex": RegexFilter(),
        "composite": CompositeFilter(),
    }

    @classmethod
    def resolve(cls, key):
        if callable(key):
            return key
        return cls._registry.get(str(key), CompositeFilter())
