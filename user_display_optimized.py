"""Compatibility wrapper keeping original API but using the new modular package.

Functions preserved: display_users, get_user_by_id, filter_users, export_users_to_string

The wrapper accepts the same arguments and delegates to `user_display` package internals.
"""
from user_display import display_users as _display
from user_display import get_user_by_id as _get_by_id
from user_display import filter_users as _filter
from user_display import export_users_to_string as _export


def display_users(users, show_all=True, verbose=False):
    # keep API signature; default formatter as compact
    return _display(users, show_all=show_all, verbose=verbose, formatter="compact")


def get_user_by_id(users, uid):
    return _get_by_id(users, uid)


def filter_users(users, criteria):
    # keep old single-arg parallel off behaviour
    return _filter(users, criteria, parallel=False)


def export_users_to_string(users):
    return _export(users, fmt="table")
