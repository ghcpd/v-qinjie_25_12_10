from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format_many(self, users, show_all=True, export=False):
        pass

    @abstractmethod
    def format_one(self, user):
        pass
