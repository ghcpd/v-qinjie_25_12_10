from .base import BaseFilter

class CompositeFilter(BaseFilter):
    def __init__(self, filters, op='and'):
        self.filters = list(filters)
        self.op = op

    def match(self, user):
        if self.op == 'and':
            return all(f.match(user) for f in self.filters)
        if self.op == 'or':
            return any(f.match(user) for f in self.filters)
        raise ValueError('Unknown op')