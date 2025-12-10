"""Compatibility wrapper preserving the original public API.

This module forwards calls to the new modular implementation while keeping
function signatures compatible with the original baseline.
"""
from user_display import UserStore

_default_store = UserStore()


def display_users(users, show_all=True, verbose=False, fmt="compact", fields=None):
    """Display users in the requested format. Preserves original signature plus optional fmt/fields."""
    # Ignore verbose for compatibility
    return _default_store.display_users(users=users, fmt=fmt, fields=fields, show_all=show_all)


def get_user_by_id(users, uid):
    # If users is a collection, prefer fast path by building temporary store
    if isinstance(users, UserStore):
        return users.get_user_by_id(uid)
    temp = UserStore(users=users)
    return temp.get_user_by_id(uid)


def filter_users(users, criteria, parallel=False):
    if isinstance(users, UserStore):
        return users.filter_users(criteria, parallel=parallel)
    temp = UserStore(users=users)
    return temp.filter_users(criteria, parallel=parallel)


def export_users_to_string(users, fmt="json"):
    if isinstance(users, UserStore):
        return users.export_users_to_string(fmt=fmt)
    temp = UserStore(users=users)
    return temp.export_users_to_string(fmt=fmt)
