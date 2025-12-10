"""user_display package — modular, high-performance, and concurrency-safe

Public-facing convenience functions are exported here in a compatibility-preserving
way so older callers can keep using the same function names.
"""
from .store import UserStore
from .formatters import Registry as FormatterRegistry
from .filters import Registry as FilterRegistry
from .validation import default as validation_default
from .config import Config
from .logging_utils import get_logger
from .metrics import metrics

# Convenience wrappers with same signatures as baseline file.
_default_store = None


def _get_default_store():
    global _default_store
    if _default_store is None:
        _default_store = UserStore()
    return _default_store


def display_users(users, show_all=True, verbose=False, formatter="compact"):
    store = _get_default_store()
    return store.display_users(users, show_all=show_all, verbose=verbose, formatter=formatter)


def get_user_by_id(users, uid):
    store = _get_default_store()
    return store.get_user_by_id(users, uid)


def filter_users(users, criteria, parallel=False, filters=None):
    store = _get_default_store()
    return store.filter_users(users, criteria, parallel=parallel, filters=filters)


def export_users_to_string(users, fmt="table"):
    store = _get_default_store()
    return store.export_users_to_string(users, fmt=fmt)


__all__ = [
    "UserStore",
    "FormatterRegistry",
    "FilterRegistry",
    "validation_default",
    "Config",
    "get_logger",
    "metrics",
    "display_users",
    "get_user_by_id",
    "filter_users",
    "export_users_to_string",
]
