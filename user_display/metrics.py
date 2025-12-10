"""
Metrics collection and reporting for user_display module.
Tracks performance, cache hits, shard usage, validation issues, etc.
"""

import threading
from typing import Dict, Any, Optional
from collections import defaultdict
from time import time
from datetime import datetime


class Metrics:
    """
    Thread-safe metrics collector for tracking performance and system state.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self._lock = threading.RLock()
        self._counters: Dict[str, int] = defaultdict(int)
        self._timers: Dict[str, list] = defaultdict(list)
        self._gauges: Dict[str, float] = {}
        self._start_time = datetime.utcnow()
    
    def increment_counter(self, name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        with self._lock:
            self._counters[name] += value
    
    def record_timer(self, name: str, duration_ms: float) -> None:
        """Record a timer metric in milliseconds."""
        with self._lock:
            self._timers[name].append(duration_ms)
    
    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge metric to a specific value."""
        with self._lock:
            self._gauges[name] = value
    
    def get_counter(self, name: str) -> int:
        """Get the current value of a counter."""
        with self._lock:
            return self._counters.get(name, 0)
    
    def get_timer_stats(self, name: str) -> Optional[Dict[str, float]]:
        """Get statistics for a timer metric."""
        with self._lock:
            times = self._timers.get(name)
            if not times or len(times) == 0:
                return None
            
            total = sum(times)
            return {
                "count": len(times),
                "total_ms": total,
                "mean_ms": total / len(times),
                "min_ms": min(times),
                "max_ms": max(times),
                "p50_ms": sorted(times)[len(times) // 2],
                "p95_ms": sorted(times)[int(len(times) * 0.95)],
                "p99_ms": sorted(times)[int(len(times) * 0.99)],
            }
    
    def get_gauge(self, name: str) -> Optional[float]:
        """Get the current value of a gauge."""
        with self._lock:
            return self._gauges.get(name)
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._timers.clear()
            self._gauges.clear()
    
    def to_dict(self) -> Dict[str, Any]:
        """Export all metrics as a dictionary."""
        with self._lock:
            timer_stats = {}
            for name in self._timers:
                stats = self.get_timer_stats(name)
                if stats:
                    timer_stats[name] = stats
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "uptime_seconds": (datetime.utcnow() - self._start_time).total_seconds(),
                "counters": dict(self._counters),
                "timers": timer_stats,
                "gauges": dict(self._gauges),
            }
    
    def __str__(self) -> str:
        """Return a human-readable metrics summary."""
        metrics_dict = self.to_dict()
        lines = []
        lines.append("=== METRICS REPORT ===")
        lines.append(f"Timestamp: {metrics_dict['timestamp']}")
        lines.append(f"Uptime: {metrics_dict['uptime_seconds']:.2f}s")
        
        if metrics_dict['counters']:
            lines.append("\nCounters:")
            for name, value in sorted(metrics_dict['counters'].items()):
                lines.append(f"  {name}: {value}")
        
        if metrics_dict['timers']:
            lines.append("\nTimers (ms):")
            for name, stats in sorted(metrics_dict['timers'].items()):
                lines.append(f"  {name}:")
                lines.append(f"    count: {stats['count']}")
                lines.append(f"    mean: {stats['mean_ms']:.2f}")
                lines.append(f"    min: {stats['min_ms']:.2f}, max: {stats['max_ms']:.2f}")
                lines.append(f"    p50: {stats['p50_ms']:.2f}, p95: {stats['p95_ms']:.2f}, p99: {stats['p99_ms']:.2f}")
        
        if metrics_dict['gauges']:
            lines.append("\nGauges:")
            for name, value in sorted(metrics_dict['gauges'].items()):
                lines.append(f"  {name}: {value}")
        
        return "\n".join(lines)


# Global metrics instance
_global_metrics: Optional[Metrics] = None


def get_metrics() -> Metrics:
    """Get or create the global metrics instance."""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = Metrics()
    return _global_metrics


def reset_metrics() -> None:
    """Reset the global metrics."""
    global _global_metrics
    if _global_metrics:
        _global_metrics.reset()
