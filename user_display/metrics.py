import threading


class Metrics:
    def __init__(self):
        self._lock = threading.Lock()
        self.counters = {}

    def incr(self, key, n=1):
        with self._lock:
            self.counters[key] = self.counters.get(key, 0) + n

    def get(self, key):
        with self._lock:
            return self.counters.get(key, 0)

    def snapshot(self):
        with self._lock:
            return dict(self.counters)
