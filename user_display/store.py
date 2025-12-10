"""
Storage module for user_display.
Provides thread-safe user storage with indexing, sharding, and MVCC-like snapshotting.
"""

import threading
import copy
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import deque

from .index import UserIndex, FieldIndex
from .validation import Validator, create_default_validator
from .errors import StorageError, ValidationError
from .logging_utils import get_logger
from .metrics import get_metrics
from .config import get_config


logger = get_logger("store")
metrics = get_metrics()


class UserSnapshot:
    """Immutable snapshot of the user list at a point in time."""
    
    def __init__(self, users: List[Dict[str, Any]], version: int, timestamp: datetime):
        """
        Initialize snapshot.
        
        Args:
            users: Copy of user list
            version: Snapshot version number
            timestamp: When snapshot was created
        """
        self.users = copy.deepcopy(users)
        self.version = version
        self.timestamp = timestamp
        self.index = UserIndex(shard_count=get_config().get("shard_count", 4))
        self.index.rebuild(self.users)
    
    def get_user(self, user_id: Any) -> Optional[Dict[str, Any]]:
        """Get a user by ID from this snapshot."""
        position = self.index.lookup(user_id)
        if position is not None:
            return copy.deepcopy(self.users[position])
        return None
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get a copy of all users from this snapshot."""
        return copy.deepcopy(self.users)


class UserStore:
    """
    Thread-safe user storage with indexing, sharding, and snapshotting support.
    Provides O(1) ID lookup and optional MVCC-like concurrent reads.
    """
    
    def __init__(self, validator: Optional[Validator] = None):
        """
        Initialize user store.
        
        Args:
            validator: Optional validator for user records (default: create_default_validator)
        """
        self._users: List[Dict[str, Any]] = []
        self._lock = threading.RLock()
        self._index = UserIndex(shard_count=get_config().get("shard_count", 4))
        self._field_indices: Dict[str, FieldIndex] = {}
        self._validator = validator or create_default_validator()
        self._version = 0
        self._snapshots: deque = deque(
            maxlen=get_config().get("snapshot_max_versions", 10)
        )
        self._validation_issues: List[Tuple[int, List[str]]] = []
    
    def add_user(self, user: Dict[str, Any], validate: bool = True) -> Tuple[bool, List[str]]:
        """
        Add a user to the store.
        
        Args:
            user: User dictionary
            validate: Whether to validate before adding
        
        Returns:
            Tuple of (success, list_of_validation_issues)
        """
        issues = []
        
        # Validation
        if validate:
            is_valid, validation_issues = self._validator.validate(user)
            issues.extend(validation_issues)
            
            if not is_valid and get_config().get("strict_validation", False):
                logger.error("Validation failed for user", user_id=user.get("id"), issues=issues)
                return False, issues
        
        with self._lock:
            position = len(self._users)
            
            # Add user
            user_copy = copy.deepcopy(user)
            self._users.append(user_copy)
            
            # Update indices
            user_id = user.get("id")
            if user_id is not None:
                self._index.add(user_id, position)
            
            # Update field indices
            for field_name, field_index in self._field_indices.items():
                field_value = user.get(field_name)
                field_index.add(field_value, user_id)
            
            # Track validation issues
            if issues:
                self._validation_issues.append((position, issues))
                logger.warning("User added with validation issues", user_id=user_id, issues=issues)
            
            # Create snapshot after modification
            self._create_snapshot()
            
            metrics.increment_counter("users_added")
            return True, issues
    
    def add_users(self, users: List[Dict[str, Any]], validate: bool = True) -> Tuple[int, List[Tuple[int, List[str]]]]:
        """
        Add multiple users to the store.
        
        Args:
            users: List of user dictionaries
            validate: Whether to validate before adding
        
        Returns:
            Tuple of (num_added, list_of_failed_indices_and_issues)
        """
        failed = []
        count = 0
        
        for idx, user in enumerate(users):
            success, issues = self.add_user(user, validate=validate)
            if not success:
                failed.append((idx, issues))
            else:
                count += 1
        
        return count, failed
    
    def get_user(self, user_id: Any) -> Optional[Dict[str, Any]]:
        """Get a user by ID. O(1) complexity."""
        with self._lock:
            start = datetime.utcnow()
            position = self._index.lookup(user_id)
            
            if position is not None:
                user = copy.deepcopy(self._users[position])
                duration = (datetime.utcnow() - start).total_seconds() * 1000
                metrics.record_timer("lookup_duration_ms", duration)
                metrics.increment_counter("lookups")
                return user
        
        metrics.increment_counter("lookup_misses")
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get a copy of all users."""
        with self._lock:
            return copy.deepcopy(self._users)
    
    def filter_by_field(self, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        """
        Filter users by field value using field index.
        Returns a copy of matching users.
        """
        if field_name not in self._field_indices:
            # Fallback to linear search
            with self._lock:
                return [copy.deepcopy(u) for u in self._users if u.get(field_name) == field_value]
        
        field_index = self._field_indices[field_name]
        user_ids = field_index.lookup(field_value)
        
        result = []
        with self._lock:
            for user_id in user_ids:
                position = self._index.lookup(user_id)
                if position is not None:
                    result.append(copy.deepcopy(self._users[position]))
        
        return result
    
    def create_field_index(self, field_name: str) -> None:
        """Create a secondary index for efficient field-based filtering."""
        with self._lock:
            if field_name not in self._field_indices:
                field_index = FieldIndex(field_name)
                for user in self._users:
                    user_id = user.get("id")
                    field_value = user.get(field_name)
                    field_index.add(field_value, user_id)
                self._field_indices[field_name] = field_index
    
    def _create_snapshot(self) -> None:
        """Create a new snapshot of the current state."""
        if get_config().get("enable_snapshotting", True):
            self._version += 1
            snapshot = UserSnapshot(self._users, self._version, datetime.utcnow())
            self._snapshots.append(snapshot)
            metrics.set_gauge("snapshot_count", len(self._snapshots))
    
    def get_snapshot(self, version: Optional[int] = None) -> Optional[UserSnapshot]:
        """Get a snapshot by version (None = latest)."""
        with self._lock:
            if not self._snapshots:
                return None
            
            if version is None:
                return self._snapshots[-1]
            
            for snapshot in self._snapshots:
                if snapshot.version == version:
                    return snapshot
            
            return None
    
    def get_validation_issues(self) -> List[Tuple[int, List[str]]]:
        """Get all recorded validation issues."""
        with self._lock:
            return copy.deepcopy(self._validation_issues)
    
    def clear_validation_issues(self) -> None:
        """Clear validation issue records."""
        with self._lock:
            self._validation_issues.clear()
    
    def size(self) -> int:
        """Get the number of users in the store."""
        with self._lock:
            return len(self._users)
    
    def clear(self) -> None:
        """Clear all users and indices."""
        with self._lock:
            self._users.clear()
            self._index.clear()
            for field_index in self._field_indices.values():
                field_index.clear()
            self._validation_issues.clear()
            self._snapshots.clear()
            self._version = 0
