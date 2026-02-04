import threading
from copy import deepcopy
from collections import defaultdict
from .errors import NotFoundError


class UserStore:
    """Thread-safe user store with O(1) id lookup and snapshot support."""

    def __init__(self, users=None):
        self._lock = threading.RLock()
        self._users = []
        self._by_id = {}
        if users:
            self.replace_all(users)

    def replace_all(self, users):
        with self._lock:
            self._users = list(users)
            self._by_id = {u.get("id"): u for u in self._users}

    def snapshot(self):
        # Return a shallow copy of list to allow concurrent reads
        with self._lock:
            return list(self._users)

    def get_by_id(self, uid):
        with self._lock:
            u = self._by_id.get(uid)
            if u is None:
                return None
            # shallow copy is sufficient and faster than deepcopy
            return dict(u)

    def add_user(self, user):
        with self._lock:
            uid = user.get("id")
            if uid in self._by_id:
                raise ValueError("duplicate id")
            self._users.append(user)
            self._by_id[uid] = user

    def update_user(self, uid, **fields):
        with self._lock:
            if uid not in self._by_id:
                raise NotFoundError(uid)
            user = self._by_id[uid]
            user.update(fields)

    def delete_user(self, uid):
        with self._lock:
            if uid not in self._by_id:
                raise NotFoundError(uid)
            user = self._by_id.pop(uid)
            self._users.remove(user)
