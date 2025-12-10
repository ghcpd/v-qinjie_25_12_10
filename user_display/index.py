"""
Indexing module for user_display.
Provides O(1) ID lookup via hash-based indexing with optional sharding support.
"""

import threading
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict


class UserIndex:
    """
    Thread-safe index for O(1) user lookup by ID.
    Supports optional sharding for distributed scenarios.
    """
    
    def __init__(self, shard_count: int = 1):
        """
        Initialize user index.
        
        Args:
            shard_count: Number of shards for distributed lookup (default: 1, no sharding)
        """
        self.shard_count = max(1, shard_count)
        self._shards: List[Dict[Any, int]] = [
            {} for _ in range(self.shard_count)
        ]
        self._locks: List[threading.RLock] = [
            threading.RLock() for _ in range(self.shard_count)
        ]
        self._size = 0
        self._global_lock = threading.RLock()
    
    def _get_shard_index(self, user_id: Any) -> int:
        """Determine which shard a user ID belongs to."""
        return hash(user_id) % self.shard_count
    
    def add(self, user_id: Any, position: int) -> None:
        """
        Add a user to the index.
        
        Args:
            user_id: The user's ID
            position: The position in the user list
        """
        shard_idx = self._get_shard_index(user_id)
        with self._locks[shard_idx]:
            if user_id not in self._shards[shard_idx]:
                with self._global_lock:
                    self._size += 1
            self._shards[shard_idx][user_id] = position
    
    def remove(self, user_id: Any) -> None:
        """Remove a user from the index."""
        shard_idx = self._get_shard_index(user_id)
        with self._locks[shard_idx]:
            if user_id in self._shards[shard_idx]:
                del self._shards[shard_idx][user_id]
                with self._global_lock:
                    self._size -= 1
    
    def lookup(self, user_id: Any) -> Optional[int]:
        """
        Look up a user by ID.
        
        Returns:
            The user's position in the list, or None if not found
        """
        shard_idx = self._get_shard_index(user_id)
        with self._locks[shard_idx]:
            return self._shards[shard_idx].get(user_id)
    
    def exists(self, user_id: Any) -> bool:
        """Check if a user exists in the index."""
        shard_idx = self._get_shard_index(user_id)
        with self._locks[shard_idx]:
            return user_id in self._shards[shard_idx]
    
    def get_all_ids(self) -> List[Any]:
        """Get all indexed user IDs."""
        result = []
        for shard in self._shards:
            with self._locks[self._shards.index(shard)]:
                result.extend(shard.keys())
        return result
    
    def size(self) -> int:
        """Get the number of indexed users."""
        with self._global_lock:
            return self._size
    
    def clear(self) -> None:
        """Clear all indices."""
        for shard in self._shards:
            shard.clear()
        with self._global_lock:
            self._size = 0
    
    def rebuild(self, users: List[Dict[str, Any]], id_field: str = "id") -> None:
        """
        Rebuild the index from a user list.
        
        Args:
            users: List of user dictionaries
            id_field: The field name to use as ID (default: "id")
        """
        self.clear()
        for position, user in enumerate(users):
            user_id = user.get(id_field)
            if user_id is not None:
                self.add(user_id, position)


class FieldIndex:
    """
    Secondary index for field-based lookup.
    Maps field values to sets of user IDs for efficient filtering.
    """
    
    def __init__(self, field_name: str):
        """
        Initialize field index.
        
        Args:
            field_name: The field to index
        """
        self.field_name = field_name
        self._index: Dict[Any, Set[Any]] = defaultdict(set)
        self._lock = threading.RLock()
    
    def add(self, field_value: Any, user_id: Any) -> None:
        """Add a user to the field index."""
        if field_value is not None:
            with self._lock:
                self._index[field_value].add(user_id)
    
    def remove(self, field_value: Any, user_id: Any) -> None:
        """Remove a user from the field index."""
        if field_value is not None:
            with self._lock:
                if field_value in self._index:
                    self._index[field_value].discard(user_id)
                    if not self._index[field_value]:
                        del self._index[field_value]
    
    def lookup(self, field_value: Any) -> Set[Any]:
        """
        Look up user IDs by field value.
        
        Returns:
            Set of user IDs with the given field value
        """
        with self._lock:
            return set(self._index.get(field_value, set()))
    
    def clear(self) -> None:
        """Clear the field index."""
        with self._lock:
            self._index.clear()
