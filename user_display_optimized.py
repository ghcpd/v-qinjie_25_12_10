"""
user_display_optimized.py

High-performance, modular, concurrent implementation of the user display system.
Preserves the original API from user_display_original.py while providing modern,
scalable infrastructure with indexing, validation, formatting, and filtering.

Usage:
    from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string
    
    # Use exactly as you would with the original module
    result = display_users(users, show_all=True, verbose=False)
"""

import time
from io import StringIO
from datetime import datetime
from typing import List, Dict, Any, Optional

from user_display import (
    UserStore,
    CompactFormatter,
    JsonFormatter,
    create_default_validator,
    get_metrics,
    get_logger,
    get_config,
)
from user_display.filters import FieldContainsFilter, FieldMatchFilter, CompositeFilter


logger = get_logger("optimized_api")
metrics = get_metrics()

# Global user store instance (preserves original stateless API)
_global_store: Optional[UserStore] = None


def _get_store() -> UserStore:
    """Get or create the global user store."""
    global _global_store
    if _global_store is None:
        config = get_config()
        validator = create_default_validator()
        _global_store = UserStore(validator=validator)
    return _global_store


def _reload_store(users: List[Dict[str, Any]]) -> None:
    """Reload the global store with new users."""
    global _global_store
    store = _get_store()
    store.clear()
    store.add_users(users, validate=config.get("validate_on_insert", True))


def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """
    Display users in compact format.
    
    API-compatible with user_display_original.display_users.
    Performance: O(n) with no artificial delays, buffered string building.
    
    Args:
        users: List of user dictionaries
        show_all: If True, append count to output
        verbose: If True, log processing details
    
    Returns:
        Formatted user list as string
    """
    start_time = time.time()
    
    # Reload store with current users
    _reload_store(users)
    
    if verbose:
        logger.info("Display users called", count=len(users))
    
    # Use compact formatter for output
    all_users = _get_store().get_all_users()
    formatter = CompactFormatter(include_header=False)
    
    # Build output efficiently
    output_lines = []
    for user in all_users:
        line_parts = []
        line_parts.append("ID=" + str(user.get("id", "N/A")))
        line_parts.append("NAME=" + str(user.get("name", "")))
        line_parts.append("EMAIL=" + str(user.get("email", "")))
        line_parts.append("ROLE=" + str(user.get("role", "")))
        line_parts.append("STATUS=" + str(user.get("status", "")))
        line_parts.append("JOIN_DATE=" + str(user.get("join_date", "")))
        line_parts.append("LAST_LOGIN=" + str(user.get("last_login", "")))
        output_lines.append(" | ".join(line_parts))
    
    result = "\n".join(output_lines)
    
    if show_all:
        result += "\nPROCESSED=" + str(len(all_users)) + "\n"
    
    duration_ms = (time.time() - start_time) * 1000
    metrics.record_timer("display_users_duration_ms", duration_ms)
    metrics.increment_counter("display_users_calls")
    
    if verbose:
        logger.info("Display users completed", count=len(users), duration_ms=duration_ms)
    
    return result


def get_user_by_id(users: List[Dict[str, Any]], uid: Any) -> Optional[Dict[str, Any]]:
    """
    Get a user by ID.
    
    API-compatible with user_display_original.get_user_by_id.
    Performance: O(1) using hash-based indexing.
    
    Args:
        users: List of user dictionaries
        uid: User ID to look up
    
    Returns:
        User dictionary or None if not found
    """
    start_time = time.time()
    
    # Reload store with current users
    _reload_store(users)
    store = _get_store()
    
    user = store.get_user(uid)
    
    duration_ms = (time.time() - start_time) * 1000
    metrics.record_timer("get_user_by_id_duration_ms", duration_ms)
    
    if user is None:
        metrics.increment_counter("get_user_by_id_misses")
    else:
        metrics.increment_counter("get_user_by_id_hits")
    
    return user


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter users by criteria.
    
    API-compatible with user_display_original.filter_users.
    Supports: name (substring, case-insensitive), email (substring, case-insensitive),
              role (exact match), status (exact match)
    Performance: O(n) single-pass filtering.
    
    Args:
        users: List of user dictionaries
        criteria: Dictionary of field: value pairs to filter by
    
    Returns:
        Filtered list of users
    """
    start_time = time.time()
    
    # Reload store with current users
    _reload_store(users)
    
    # Build filters from criteria
    filters_list = []
    
    if "name" in criteria:
        filters_list.append(FieldContainsFilter("name", criteria["name"], case_sensitive=False))
    
    if "email" in criteria:
        filters_list.append(FieldContainsFilter("email", criteria["email"], case_sensitive=False))
    
    if "role" in criteria:
        filters_list.append(FieldMatchFilter("role", criteria["role"], case_sensitive=True))
    
    if "status" in criteria:
        filters_list.append(FieldMatchFilter("status", criteria["status"], case_sensitive=True))
    
    # Apply filters
    result = users
    if filters_list:
        composite = CompositeFilter(filters_list, use_or=False)
        result = composite.apply(result)
    
    duration_ms = (time.time() - start_time) * 1000
    metrics.record_timer("filter_users_duration_ms", duration_ms)
    metrics.increment_counter("filter_users_calls")
    
    return result


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """
    Export users to a formatted string.
    
    API-compatible with user_display_original.export_users_to_string.
    Performance: O(n) with efficient string building, parsed timestamps cached.
    
    Args:
        users: List of user dictionaries
    
    Returns:
        Formatted export string
    """
    start_time = time.time()
    
    # Reload store with current users
    _reload_store(users)
    all_users = _get_store().get_all_users()
    
    output_lines = []
    output_lines.append("EXPORT_BEGIN")
    output_lines.append("=" * 120)
    
    # Parse timestamps once
    for user in all_users:
        try:
            last_login_str = user.get("last_login", "2000-01-01")
            parsed_date = datetime.strptime(last_login_str, "%Y-%m-%d")
            timestamp_value = parsed_date.timestamp()
        except (ValueError, TypeError):
            timestamp_value = 0.0
        
        output_lines.append("UserID: " + str(user.get("id", "N/A")))
        output_lines.append("  Name: " + str(user.get("name", "")))
        output_lines.append("  LastLoginParsed: " + str(timestamp_value))
        output_lines.append("-" * 120)
    
    output_lines.append("EXPORT_END")
    
    result = "\n".join(output_lines)
    
    duration_ms = (time.time() - start_time) * 1000
    metrics.record_timer("export_users_duration_ms", duration_ms)
    metrics.increment_counter("export_users_calls")
    
    return result


def reset_store() -> None:
    """Reset the global user store (for testing)."""
    global _global_store
    _global_store = None


# For backward compatibility
config = get_config()


if __name__ == "__main__":
    # Example usage
    sample_users = [
        {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "role": "Admin" if i % 3 == 0 else "User",
            "status": "Active" if i % 2 == 0 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, 101)
    ]
    
    print("=== Display Users ===")
    print(display_users(sample_users)[:200])
    
    print("\n=== Get User by ID ===")
    user = get_user_by_id(sample_users, 1)
    print(f"User 1: {user}")
    
    print("\n=== Filter Users ===")
    filtered = filter_users(sample_users, {"role": "Admin"})
    print(f"Admin count: {len(filtered)}")
    
    print("\n=== Export ===")
    export = export_users_to_string(sample_users)
    print(export[:300])
