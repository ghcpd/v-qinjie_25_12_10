import time
from threading import Lock


class Metrics:
    def __init__(self):
        self._counters = {}
        self._timers = {}
        self._lock = Lock()

    def increment(self, name, amount=1):
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount

    def record(self, name, value):
        with self._lock:
            self._timers[name] = value

    def snapshot(self):
        with self._lock:
            return {"counters": dict(self._counters), "timers": dict(self._timers)}


metrics = Metrics()
