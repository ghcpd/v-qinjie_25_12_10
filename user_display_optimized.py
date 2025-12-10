"""
Optimized compatibility wrapper that preserves original API:
- display_users(users, show_all=True, verbose=False)
- get_user_by_id(users, uid)
- filter_users(users, criteria)
- export_users_to_string(users)

Internally uses user_display package (store, formatters, validation, filters).
"""
from user_display import UserStore, DefaultValidator
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JsonFormatter
from user_display.formatters.table import TableFormatter
from user_display.filters.regex_filter import RegexFilter
from user_display.validation.default import DefaultValidator as ValidatorClass
from user_display.logging_utils import struct_log
from user_display.metrics import GLOBAL as METRICS
import time

# Helpers

def _ensure_store(users):
    if isinstance(users, UserStore):
        return users
    # if it's already a snapshot-like dict (from store.snapshot), use it
    if isinstance(users, dict) and 'users' in users:
        return UserStore(users=users['users'])
    # otherwise assume it's a list
    return UserStore(users=users)


def display_users(users, show_all=True, verbose=False, formatter='compact'):
    """Improved display: buffered, sanitized, deterministic, fast."""
    start = time.perf_counter()
    store = _ensure_store(users)
    user_list = store.list_users()
    if verbose:
        for u in user_list:
            struct_log('debug', 'BEGIN_PROCESS_USER', user_id=u.get('id'))
    # choose formatter
    if formatter == 'json':
        fmt = JsonFormatter()
    elif formatter == 'table':
        fmt = TableFormatter()
    else:
        fmt = CompactFormatter()
    out = fmt.format_many(user_list, show_all=show_all)
    METRICS.timeit('display_users', time.perf_counter() - start)
    return out


def get_user_by_id(users, uid):
    """O(1) lookup via index if available."""
    store = _ensure_store(users)
    return store.get_user_by_id(uid)


def filter_users(users, criteria, use_cache=True, parallel=False):
    """Basic criteria dict support with efficient single-pass filtering.

    criteria keys: name (substring, case-insensitive), email (substring), role, status
    """
    store = _ensure_store(users)
    # simple fast path if criteria is callable
    if callable(criteria):
        # treat as predicate
        filtered = [u for u in store.list_users() if criteria(u)]
        return filtered
    # build composite predicate
    name = criteria.get('name') if isinstance(criteria, dict) else None
    email = criteria.get('email') if isinstance(criteria, dict) else None
    role = criteria.get('role') if isinstance(criteria, dict) else None
    status = criteria.get('status') if isinstance(criteria, dict) else None

    users_list = store.list_users()
    res = []
    if name:
        nl = name.lower()
        for u in users_list:
            if nl in (u.get('name') or '').lower():
                if email and email not in (u.get('email') or ''):
                    continue
                if role and u.get('role') != role:
                    continue
                if status and u.get('status') != status:
                    continue
                res.append(u)
    else:
        for u in users_list:
            if email and email not in (u.get('email') or ''):
                continue
            if role and u.get('role') != role:
                continue
            if status and u.get('status') != status:
                continue
            res.append(u)
    # store cache
    if use_cache:
        try:
            store._cache[repr(criteria)] = res
        except Exception:
            pass
    return res


def export_users_to_string(users, formatter='compact', max_lines=None):
    """Export users with sanitized dates and deterministic order.

    Preserves API: returns a string. Avoids heavy repeated parsing and randomness.
    """
    store = _ensure_store(users)
    user_list = store.list_users()
    # sort by id for deterministic output
    try:
        user_list = sorted(user_list, key=lambda x: (x.get('id') is None, x.get('id')))
    except Exception:
        pass
    # choose formatter behavior: by default produce a readable block similar to original export
    max_lines = max_lines or None
    lines = []
    header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
    lines.append(header)
    count = 0
    for u in user_list:
        if max_lines and count >= max_lines:
            break
        # use stored timestamp if present
        last_ts = u.get('_last_login_ts', None)
        lines.append(f"UserID: {u.get('id','N/A')}\n")
        lines.append(f"  Name: {u.get('name','')}\n")
        lines.append(f"  LastLoginTS: {last_ts if last_ts is not None else u.get('last_login','')}\n")
        lines.append("-" * 120 + "\n")
        count += 1
    lines.append("EXPORT_END\n")
    return ''.join(lines)


# maintain legacy sample_users for convenience
sample_users = [
    {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@example.com",
        "role": "Admin" if i % 10 == 0 else "User",
        "status": "Active" if i % 3 != 0 else "Inactive",
        "join_date": "2023-01-01",
        "last_login": "2025-11-26",
    }
    for i in range(1, 101)
]
