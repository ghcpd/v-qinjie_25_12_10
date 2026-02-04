from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    def matches(self, user):
        pass

    def apply(self, users, limit=None):
        res = []
        for u in users:
            if self.matches(u):
                res.append(u)
                if limit and len(res) >= limit:
                    break
        return res
