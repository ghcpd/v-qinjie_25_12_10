from .base import BaseFilter


class CompositeFilter(BaseFilter):
    def __init__(self, filters):
        self.filters = filters

    def match(self, user):
        for f in self.filters:
            if not f.match(user):
                return False
        return True
