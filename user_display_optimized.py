"""
Optimized user display module with backward compatibility.
"""

import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any
from user_display import (
    UserStore, BaseFormatter, JSONFormatter, TableFormatter, CompactFormatter,
    BaseFilter, RegexFilter, CompositeFilter, config, logger, metrics
)

# Global store instance
_store = UserStore()

# Cache to avoid re-adding users
_user_cache = None  # Will store (len(users), users[0]['id']) if added

def _ensure_users_added(users: List[Dict[str, Any]]):
    """Ensure users are added to store, with caching to avoid duplicates."""
    global _user_cache
    if not users:
        return
    cache_key = (len(users), users[0].get('id'))
    if _user_cache == cache_key:
        return  # Already added
    _store.add_users(users)
    _user_cache = cache_key

def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False, format_type: str = 'default') -> str:
    """
    Display users in the specified format.
    Compatible with original API, but adds format_type parameter.
    """
    start_time = time.time()

    # Add users to store if not already
    _ensure_users_added(users)

    # Select formatter
    if format_type == 'json':
        formatter = JSONFormatter()
    elif format_type == 'table':
        formatter = TableFormatter()
    elif format_type == 'compact':
        formatter = CompactFormatter()
    else:
        formatter = BaseFormatter()

    # Format
    result = formatter.format_users(users)

    if show_all:
        result += f"\nPROCESSED={len(users)}\n"

    duration = time.time() - start_time
    metrics.timer('display_users', duration)
    logger.info("Displayed users", count=len(users), format=format_type, duration=duration)

    return result

def get_user_by_id(users: List[Dict[str, Any]], uid: int) -> Dict[str, Any] | None:
    """
    Get user by ID. Uses store for O(1) lookup.
    """
    _ensure_users_added(users)  # Ensure in store
    user = _store.get_user_by_id(uid)
    if user:
        metrics.increment('id_lookups_success')
    else:
        metrics.increment('id_lookups_miss')
    return user

def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter users based on criteria.
    Supports parallel filtering if enabled.
    """
    start_time = time.time()

    _ensure_users_added(users)

    # Create filter
    filter_obj = BaseFilter(criteria)

    if config.get('parallel_filtering', False) and len(users) > 1000:  # Disabled for performance
        # Parallel filtering
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(filter_obj.matches, u) for u in users]
            matches = [u for u, f in zip(users, futures) if f.result()]
    else:
        matches = [u for u in users if filter_obj.matches(u)]

    duration = time.time() - start_time
    metrics.timer('filter_users', duration, tags={'parallel': config.get('parallel_filtering', True)})
    logger.info("Filtered users", total=len(users), filtered=len(matches), duration=duration)

    return matches

def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to string with timestamps.
    Optimized to avoid repeated parsing.
    """
    start_time = time.time()

    _ensure_users_added(users)

    lines = []
    lines.append("EXPORT_BEGIN")
    lines.append("=" * 120)

    for user in users:
        uid = user.get('id', 'N/A')
        name = user.get('name', '')
        last_login_str = user.get('last_login', '2000-01-01')
        try:
            # Parse once
            dt = datetime.strptime(last_login_str, "%Y-%m-%d")
            timestamp = dt.timestamp()
        except ValueError:
            timestamp = 0.0

        lines.append(f"UserID: {uid}")
        lines.append(f"  Name: {name}")
        lines.append(f"  LastLoginParsed: {timestamp}")
        lines.append("-" * 120)

    lines.append("EXPORT_END")

    result = '\n'.join(lines) + '\n'

    duration = time.time() - start_time
    metrics.timer('export_users', duration)
    logger.info("Exported users", count=len(users), duration=duration)

    return result

# For testing, expose the store
def get_store():
    return _store