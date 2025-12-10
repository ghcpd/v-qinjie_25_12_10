"""
Compatibility wrapper exposing the original public API while using the new modular implementation.
Preserves: display_users, get_user_by_id, filter_users, export_users_to_string
"""
from user_display.store import UserStore
from user_display.formatters.json_fmt import JsonFormatter
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.table import TableFormatter
from user_display.filters.composite_filter import CompositeFilter
from user_display.validation.default import DefaultValidator
from user_display.plugins import plugin_manager
from user_display.logging_utils import get_logger
from user_display.metrics import Metrics

logger = get_logger(__name__)
metrics = Metrics()

# Default global store used by wrapper functions
_global_store = None


def _ensure_store(users=None):
    global _global_store
    if _global_store is None:
        _global_store = UserStore(users or [])
    elif users is not None:
        _global_store.replace_all(users)
    return _global_store


def display_users(users, show_all=True, verbose=False, profile="compact"):
    store = _ensure_store(users)
    fmt = {
        "compact": CompactFormatter(),
        "json": JsonFormatter(),
        "table": TableFormatter(),
    }.get(profile, CompactFormatter())
    validator = DefaultValidator()

    # Get snapshot for consistent read
    snapshot = store.snapshot()
    items = [validator.validate(u) for u in snapshot]
    result = fmt.format_many(items, show_all=show_all)
    if verbose:
        logger.info("displayed %d users", len(items))
    return result


def get_user_by_id(users, uid):
    # If users is a UserStore already, use fast lookup
    if isinstance(users, UserStore):
        return users.get_by_id(uid)
    # If it's a plain list, do a single-pass scan (avoids rebuilding global index)
    if isinstance(users, list):
        for u in users:
            if u.get("id") == uid:
                return u
        return None
    # Fallback to global store
    store = _ensure_store(users)
    return store.get_by_id(uid)


def filter_users(users, criteria, parallel=False, limit=None):
    store = _ensure_store(users)
    snapshot = store.snapshot()
    comp = CompositeFilter.from_criteria(criteria)
    return comp.apply(snapshot, parallel=parallel, limit=limit)


def export_users_to_string(users, profile="json"):
    store = _ensure_store(users)
    snapshot = store.snapshot()
    fmt = JsonFormatter() if profile == "json" else TableFormatter()
    return fmt.format_many(snapshot, export=True)
