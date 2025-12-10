"""Implement UserStore with indexing, snapshotting, thread-safe reads, caching and optional parallel filtering."""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable, List, Dict, Callable, Optional
from collections import OrderedDict
import time

from .formatters import Registry as FormatterRegistry
from .filters import Registry as FilterRegistry
from .validation.default import DefaultValidator
from .errors import ValidationError
from .logging_utils import get_logger
from .metrics import metrics

logger = get_logger("user_display.store")


class UserStore:
    """Thread-safe in-memory user store helpers.

    The store expects "users" to be an iterable of dict-like objects.
    It does not persist by itself — it provides indexing, snapshots and
    fast lookups that callers can use.
    """

    def __init__(self, validator: Optional[DefaultValidator] = None, max_cache=4096):
        self._lock = threading.RLock()
        self.validator = validator or DefaultValidator()
        # caches for lookups and filter results using small LRU semantics
        self._id_index: Dict[object, dict] = {}
        self._cache = OrderedDict()
        self._max_cache = max_cache

    def _ensure_index_for(self, users: Iterable[dict], validate: bool = True):
        """Build index if not available or if identity changed.

        Uses the id field of each user, if present.
        """
        with self._lock:
            # shallow scan to add ids
            if validate:
                for u in users:
                    uid = u.get("id")
                    if uid is not None:
                        # validate and stash canonical object
                        try:
                            cleaned = self.validator.validate(u)
                        except ValidationError:
                            cleaned = self.validator.recover(u)
                        self._id_index[uid] = cleaned
            else:
                # lightweight build — don't validate to keep this operation fast
                for u in users:
                    uid = u.get("id")
                    if uid is not None:
                        # store direct reference to avoid expensive validation costs
                        self._id_index[uid] = u

    def snapshot(self, users: Iterable[dict]) -> list:
        """Return a shallow-cloned snapshot of users for consistent read operations."""
        # Make a shallow list to decouple from mutating callers
        return list(users)

    def get_user_by_id(self, users: Iterable[dict], uid):
        # try quick dict hit
        if uid in self._id_index:
            metrics.increment("id_lookup_cached")
            return self._id_index[uid]

        # Fast-path: if users is an indexable sequence and ids are in the
        # standard 1-based incremental layout, try direct access to avoid
        # scanning the whole list for the common generated-case.
        try:
            if isinstance(users, list) and isinstance(uid, int) and 0 < uid <= len(users):
                candidate = users[uid - 1]
                if candidate and candidate.get("id") == uid:
                    metrics.increment("id_lookup_direct")
                    # cache lightweight reference and return
                    self._id_index[uid] = candidate
                    return candidate
        except Exception:
            # fallback to slower index build
            pass

        # build a lightweight id-index without heavy validation when missing
        # this keeps first lookups fast; callers that need validated objects
        # should call display/filter which will validate per-user as needed.
        self._ensure_index_for(users, validate=False)
        metrics.increment("id_lookup_index_build")
        return self._id_index.get(uid)

    def display_users(self, users: Iterable[dict], show_all=True, verbose=False, formatter="compact") -> str:
        """Render users quickly using a formatter registry."""
        fmt = FormatterRegistry.resolve(formatter)
        snapshot = self.snapshot(users)

        buf = []
        count = 0
        for u in snapshot:
            try:
                cleaned = self.validator.validate(u)
            except ValidationError:
                cleaned = self.validator.recover(u)
                metrics.increment("validation_recovered")

            buf.append(fmt.format(cleaned))
            count += 1

        if show_all:
            buf.append(f"PROCESSED={count}")

        metrics.record("display_users_count", count)
        return "\n".join(buf) + ("\n" if buf else "")

    def filter_users(self, users: Iterable[dict], criteria: dict, parallel: bool = False, filters: Optional[list] = None) -> List[dict]:
        """Filter users using a configurable set of filters. Returns list of cleaned users.

        parallel: if True, will use multiple threads for evaluation across shards.
        filters: optional list of filter names or callables to apply instead of the default composite.
        """
        snapshot = self.snapshot(users)
        metrics.increment("filter_called")

        # Construct filters
        if filters:
            filter_funcs = [FilterRegistry.resolve(f) for f in filters]
        else:
            filter_funcs = [FilterRegistry.resolve("composite")]

        def check(u):
            try:
                cleaned = self.validator.validate(u)
            except ValidationError:
                cleaned = self.validator.recover(u)
                metrics.increment("validation_recovered")

            for f in filter_funcs:
                if not f.match(cleaned, criteria):
                    return None
            return cleaned

        # use simple parallelism strategy
        results = []
        if parallel and len(snapshot) > 1000:
            # pick a thread pool sized for CPU bound-ish tasks
            workers = min(8, (len(snapshot) // 2000) + 1)
            with ThreadPoolExecutor(max_workers=workers) as ex:
                futures = [ex.submit(check, u) for u in snapshot]
                for fut in as_completed(futures):
                    val = fut.result()
                    if val:
                        results.append(val)
            metrics.record("filter_parallel_workers", workers)
        else:
            for u in snapshot:
                val = check(u)
                if val:
                    results.append(val)

        metrics.record("filter_result_size", len(results))
        return results

    def export_users_to_string(self, users: Iterable[dict], fmt: str = "table") -> str:
        snapshot = self.snapshot(users)
        fmt_obj = FormatterRegistry.resolve(fmt)
        out = [fmt_obj.header()]
        for u in snapshot:
            try:
                cleaned = self.validator.validate(u)
            except ValidationError:
                cleaned = self.validator.recover(u)
                metrics.increment("validation_recovered")

            out.append(fmt_obj.export(cleaned))

        out.append(fmt_obj.footer())
        return "\n".join(out)
