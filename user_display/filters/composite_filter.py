from .base import BaseFilter
from .regex_filter import RegexFilter
from concurrent.futures import ThreadPoolExecutor
import re


class CompositeFilter(BaseFilter):
    def __init__(self, filters=None):
        self.filters = filters or []

    @classmethod
    def from_criteria(cls, criteria):
        filters = []
        for k, v in (criteria or {}).items():
            # support simple substring criteria and regex if startswith r/
            if isinstance(v, str) and v.startswith("r/"):
                pattern = v[2:]
                filters.append(RegexFilter(k, pattern))
            else:
                filters.append(RegexFilter(k, re.escape(str(v))))
        return cls(filters)

    def matches(self, user):
        return all(f.matches(user) for f in self.filters)

    def apply(self, users, parallel=False, limit=None):
        if not parallel:
            return super().apply(users, limit=limit)
        # Parallel apply in shards
        res = []
        with ThreadPoolExecutor() as ex:
            # Use BaseFilter.apply with explicit self to avoid unbound super() in worker threads
            futures = [ex.submit(BaseFilter.apply, self, chunk, limit) for chunk in _chunk(users, 512)]
            for f in futures:
                res.extend(f.result())
                if limit and len(res) >= limit:
                    return res[:limit]
        if limit:
            return res[:limit]
        return res


def _chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i : i + size]
