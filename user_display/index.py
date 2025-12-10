"""
Indexing utilities.
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict

class UserIndex:
    """Index for fast lookups."""

    def __init__(self):
        self._id_index: Dict[int, Dict[str, Any]] = {}
        self._name_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._email_index: Dict[str, Dict[str, Any]] = {}

    def add_user(self, user: Dict[str, Any]):
        """Add user to indices."""
        uid = user.get('id')
        if uid is not None:
            self._id_index[uid] = user
        name = user.get('name', '').lower()
        self._name_index[name].append(user)
        email = user.get('email', '').lower()
        if email:
            self._email_index[email] = user

    def remove_user(self, user: Dict[str, Any]):
        """Remove user from indices."""
        uid = user.get('id')
        if uid is not None and uid in self._id_index:
            del self._id_index[uid]
        name = user.get('name', '').lower()
        if name in self._name_index:
            self._name_index[name] = [u for u in self._name_index[name] if u.get('id') != uid]
        email = user.get('email', '').lower()
        if email in self._email_index:
            del self._email_index[email]

    def get_by_id(self, uid: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        return self._id_index.get(uid)

    def get_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Get users by name."""
        return self._name_index.get(name.lower(), [])

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        return self._email_index.get(email.lower())