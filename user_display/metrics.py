"""
Metrics collection for performance monitoring.
"""

import time
from collections import defaultdict, Counter
from threading import Lock
from typing import Dict, Any
from .logging_utils import logger

class Metrics:
    """Thread-safe metrics collector."""

    def __init__(self):
        self._counters = defaultdict(Counter)
        self._timers = defaultdict(list)
        self._gauges = {}
        self._lock = Lock()

    def increment(self, name: str, value: int = 1, tags: Dict[str, Any] = None):
        """Increment a counter."""
        with self._lock:
            self._counters[name][frozenset(tags.items()) if tags else ''] += value

    def timer(self, name: str, duration: float, tags: Dict[str, Any] = None):
        """Record a timing."""
        with self._lock:
            self._timers[name].append((duration, tags))

    def gauge(self, name: str, value: Any, tags: Dict[str, Any] = None):
        """Set a gauge value."""
        with self._lock:
            self._gauges[(name, frozenset(tags.items()) if tags else '')] = value

    def time_function(self, name: str, tags: Dict[str, Any] = None):
        """Decorator to time a function."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = time.time() - start
                    self.timer(name, duration, tags)
            return wrapper
        return decorator

    def get_counters(self) -> Dict[str, Dict]:
        """Get current counter values."""
        with self._lock:
            return {k: dict(v) for k, v in self._counters.items()}

    def get_timers(self) -> Dict[str, list]:
        """Get timer data."""
        with self._lock:
            return dict(self._timers)

    def get_gauges(self) -> Dict:
        """Get gauge values."""
        with self._lock:
            return dict(self._gauges)

    def reset(self):
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._timers.clear()
            self._gauges.clear()

    def report(self):
        """Log a metrics report."""
        counters = self.get_counters()
        timers = self.get_timers()
        gauges = self.get_gauges()

        # Convert frozenset keys to strings
        counters = {k: dict(v) for k, v in counters.items()}
        for key in counters:
            counters[key] = {str(k): v for k, v in counters[key].items()}
        gauges = {str(k): v for k, v in gauges.items()}

        logger.info("Metrics Report", counters=counters, timers=timers, gauges=gauges)

# Global metrics instance
metrics = Metrics()