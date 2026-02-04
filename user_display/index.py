# Lightweight index interface (placeholder for sharding/secondary indices)
from collections import defaultdict

class Index:
    def __init__(self):
        self._by_field = defaultdict(dict)

    def add(self, user, field):
        val = user.get(field)
        if val is not None:
            self._by_field[field][val] = user

    def get(self, field, value):
        return self._by_field[field].get(value)

    def remove(self, user, field):
        val = user.get(field)
        if val in self._by_field[field]:
            del self._by_field[field][val]