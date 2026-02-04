from abc import ABC, abstractmethod

class BaseFilter(ABC):
    @abstractmethod
    def match(self, user):
        pass

    def filter_many(self, users):
        for u in users:
            if self.match(u):
                yield u