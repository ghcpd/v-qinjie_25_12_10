from threading import RLock
from copy import deepcopy
from io import StringIO
import json
from concurrent.futures import ThreadPoolExecutor

from .index import Index
from .formatters.json_fmt import JSONFormatter
from .formatters.compact import CompactFormatter
from .formatters.table import TableFormatter
from .validation.default import DefaultValidator
from .validation.base import ValidationError
from .metrics import Metrics
from .logging_utils import get_logger

logger = get_logger(__name__)


class UserStore:
    def __init__(self, users=None, config=None, max_workers=4):
        self._lock = RLock()
        self._users = [] if users is None else list(users)
        self._index = Index(self._users)
        self._validator = DefaultValidator()
        self._metrics = Metrics()
        self._config = config
        self._max_workers = max_workers
        self._cache = {}  # simple cache for filter results

    def add_users(self, users):
        with self._lock:
            idx_start = len(self._users)
            self._users.extend(users)
            self._index.add_users(users, start_index=idx_start)

    def get_user_by_id(self, uid):
        # O(1) lookup via index
        idx = self._index.id_map.get(uid)
        if idx is None:
            self._metrics.increment("lookup_miss")
            return None
        self._metrics.increment("lookup_hit")
        return deepcopy(self._users[idx])

    def filter_users(self, criteria, *, parallel=False):
        # Convert criteria to a cache key
        key = tuple(sorted(criteria.items()))
        if key in self._cache:
            self._metrics.increment("cache_hit")
            return deepcopy(self._cache[key])
        self._metrics.increment("cache_miss")

        # Fast path using indices for role/status/name prefix
        candidate_ids = None
        if "role" in criteria:
            candidate_ids = self._index.ids_for_role(criteria["role"])
        if "status" in criteria:
            ids2 = self._index.ids_for_status(criteria["status"]) 
            candidate_ids = ids2 if candidate_ids is None else candidate_ids & ids2

        users_list = []
        if candidate_ids is not None:
            users_list = [self._users[i] for i in candidate_ids]
        else:
            users_list = self._users

        matcher = None
        if "name_regex" in criteria:
            import re

            pattern = re.compile(criteria["name_regex"])

            def matcher(u):
                return bool(pattern.search(u.get("name", "")))

        def check(u):
            # other checks
            if "email" in criteria and criteria["email"] not in u.get("email", ""):
                return False
            if "name" in criteria and criteria["name"].lower() not in u.get("name", "").lower():
                return False
            if matcher and not matcher(u):
                return False
            return True

        res = []
        if parallel:
            # split into chunks
            chunks = []
            n = self._max_workers
            k = max(1, len(users_list) // n)
            for i in range(0, len(users_list), k):
                chunks.append(users_list[i : i + k])

            def scan(chunk):
                out = []
                for u in chunk:
                    if check(u):
                        out.append(u)
                return out

            with ThreadPoolExecutor(max_workers=self._max_workers) as ex:
                for part in ex.map(scan, chunks):
                    res.extend(part)
        else:
            for u in users_list:
                if check(u):
                    res.append(u)

        # cache shallow copies keyed by criteria
        self._cache[key] = list(res)
        self._metrics.increment("filtered_count", len(res))
        return deepcopy(res)

    def display_users(self, users=None, fmt="compact", fields=None, show_all=True):
        users = self._users if users is None else users
        if fmt == "compact":
            formatter = CompactFormatter(fields=fields)
        elif fmt == "json":
            formatter = JSONFormatter(fields=fields)
        elif fmt == "table":
            formatter = TableFormatter(fields=fields)
        else:
            formatter = CompactFormatter(fields=fields)

        out = formatter.format_many(users, show_all=show_all)
        return out

    def export_users_to_string(self, users=None, fmt="json"):
        users = self._users if users is None else users
        if fmt == "json":
            return JSONFormatter().format_many(users, show_all=False)
        elif fmt == "compact":
            return CompactFormatter().format_many(users, show_all=False)
        else:
            return JSONFormatter().format_many(users, show_all=False)

    def snapshot(self):
        # create shallow copy snapshot for concurrency-safe reads
        with self._lock:
            snap = deepcopy(self)
            return snap

    def clear_cache(self):
        self._cache.clear()

    def validate_and_recover(self, user):
        try:
            self._validator.validate(user)
            return user
        except ValidationError as e:
            logger.warning("Validation failed, attempting recovery: %s", e)
            recovered = self._validator.recover(user)
            self._metrics.increment("validation_recovered")
            return recovered

    def metrics(self):
        return self._metrics.snapshot()
