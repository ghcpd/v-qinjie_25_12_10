import time
from collections import Counter

class Metrics:
    def __init__(self):
        self.counters = Counter()
        self.timings = []

    def incr(self, name, n=1):
        self.counters[name] += n

    def timeit(self, fn_name, elapsed):
        self.timings.append((fn_name, elapsed))

    def snapshot(self):
        return {"counters": dict(self.counters), "timings": list(self.timings)}

GLOBAL = Metrics()