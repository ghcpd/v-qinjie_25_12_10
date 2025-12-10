from threading import RLock
from collections import defaultdict
from copy import deepcopy
from .validation.default import DefaultValidator
from .metrics import GLOBAL as METRICS
from .logging_utils import struct_log

class UserStore:
    """Thread-safe store with id index and snapshot support."""
    def __init__(self, users=None, validator=None):
        self._lock = RLock()
        self._users = list(users) if users else []
        # id -> user (sanitized)
        self._id_index = {}
        self.validator = validator or DefaultValidator()
        self._populate_index(self._users)
        self._cache = {}  # simple cache for filter results

    def _populate_index(self, users):
        for u in users:
            sanitized = self.validator.validate(u)
            self._id_index[sanitized.get('id')] = sanitized

    def add_user(self, user):
        with self._lock:
            s = self.validator.validate(user)
            self._users.append(s)
            self._id_index[s.get('id')] = s
            self._cache.clear()
            METRICS.incr('store.add')
            return s

    def get_user_by_id(self, uid):
        # O(1) lookup
        u = self._id_index.get(uid)
        if u is None:
            METRICS.incr('lookup.miss')
            return None
        METRICS.incr('lookup.hit')
        return u

    def list_users(self):
        # Return a snapshot of the list for concurrent readers
        with self._lock:
            return list(self._users)

    def snapshot(self):
        # shallow copy is acceptable since individual user dicts are small
        with self._lock:
            return {'users': list(self._users), 'index': dict(self._id_index)}

    def filter_users(self, filter_obj, use_cache=True):
        key = None
        if use_cache:
            try:
                key = repr(filter_obj)
            except Exception:
                key = None
        if key and key in self._cache:
            METRICS.incr('filter.cache_hit')
            return list(self._cache[key])
        users = self.list_users()
        res = list(filter_obj.filter_many(users))
        if key is not None:
            self._cache[key] = res
            METRICS.incr('filter.cache_store')
        METRICS.incr('filter.run')
        return res

    def update_user(self, uid, **fields):
        with self._lock:
            u = self._id_index.get(uid)
            if not u:
                return None
            u.update(fields)
            # update stored list too
            for i, orig in enumerate(self._users):
                if orig.get('id') == uid:
                    self._users[i] = u
                    break
            self._cache.clear()
            METRICS.incr('store.update')
            return u

    def remove_user(self, uid):
        with self._lock:
            u = self._id_index.pop(uid, None)
            if not u:
                return False
            self._users = [x for x in self._users if x.get('id') != uid]
            self._cache.clear()
            METRICS.incr('store.remove')
            return True


class InMemoryStore(UserStore):
    pass


DefaultValidator = DefaultValidator