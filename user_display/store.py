"""
User store with indexing and sharding.
"""

import copy
from threading import RLock
from typing import Dict, Any, List, Optional
from collections import defaultdict
from .errors import StoreError
from .validation import DefaultValidator
from .logging_utils import logger
from .metrics import metrics
from .config import config
from .index import UserIndex

class UserStore:
    """Thread-safe user store with indexing and snapshotting."""

    def __init__(self, validator=None, shard_count: int = None):
        self.validator = validator or DefaultValidator()
        self.shard_count = shard_count or config.get('shard_count', 4)
        self._shards: List[Dict[int, Dict[str, Any]]] = [{} for _ in range(self.shard_count)]
        self._indices: List[UserIndex] = [UserIndex() for _ in range(self.shard_count)]
        self._lock = RLock()
        self._snapshots: Dict[str, List[Dict[int, Dict[str, Any]]]] = {}

    def _get_shard(self, uid: int) -> int:
        """Get shard index for user ID."""
        return uid % self.shard_count

    @metrics.time_function('store_add_users')
    def add_users(self, users: List[Dict[str, Any]]):
        """Add multiple users to the store."""
        with self._lock:
            for user in users:
                self._add_user(user)

    def _add_user(self, user: Dict[str, Any]):
        """Add a single user."""
        try:
            validated = self.validator.validate(user)
            uid = validated['id']
            if uid == -1:
                raise StoreError("Invalid user ID")
            shard_idx = self._get_shard(uid)
            self._shards[shard_idx][uid] = validated
            self._indices[shard_idx].add_user(validated)
            metrics.increment('users_added')
        except Exception as e:
            logger.error("Failed to add user", user=user, error=str(e))
            metrics.increment('add_errors')

    def get_user_by_id(self, uid: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with self._lock:
            shard_idx = self._get_shard(uid)
            user = self._shards[shard_idx].get(uid)
            if user:
                metrics.increment('id_lookups', tags={'hit': True})
            else:
                metrics.increment('id_lookups', tags={'hit': False})
            return user

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        with self._lock:
            users = []
            for shard in self._shards:
                users.extend(shard.values())
            return users

    def filter_users(self, filter_func) -> List[Dict[str, Any]]:
        """Filter users using a function."""
        with self._lock:
            users = self.get_all_users()
            return [u for u in users if filter_func(u)]

    def create_snapshot(self, name: str):
        """Create a snapshot of current state."""
        with self._lock:
            self._snapshots[name] = [copy.deepcopy(shard) for shard in self._shards]
            logger.info(f"Created snapshot: {name}")

    def load_snapshot(self, name: str):
        """Load a snapshot."""
        with self._lock:
            if name not in self._snapshots:
                raise StoreError(f"Snapshot not found: {name}")
            self._shards = copy.deepcopy(self._snapshots[name])
            # Rebuild indices
            self._indices = [UserIndex() for _ in range(self.shard_count)]
            for shard in self._shards:
                for user in shard.values():
                    idx = self._get_shard(user['id'])
                    self._indices[idx].add_user(user)
            logger.info(f"Loaded snapshot: {name}")

    def clear(self):
        """Clear all users."""
        with self._lock:
            self._shards = [{} for _ in range(self.shard_count)]
            self._indices = [UserIndex() for _ in range(self.shard_count)]
            metrics.gauge('total_users', 0)