from abc import ABC, abstractmethod


class BaseFilter(ABC):
    @abstractmethod
    def match(self, user):
        pass

    def filter(self, users):
        return [u for u in users if self.match(u)]
