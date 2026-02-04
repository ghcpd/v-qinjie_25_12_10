from threading import Lock


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self._counters = {}

    def increment(self, key, amount=1):
        with self._lock:
            self._counters[key] = self._counters.get(key, 0) + amount

    def snapshot(self):
        with self._lock:
            return dict(self._counters)
