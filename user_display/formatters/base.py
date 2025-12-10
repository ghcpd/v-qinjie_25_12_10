from abc import ABC, abstractmethod

class BaseFormatter(ABC):
    @abstractmethod
    def format_many(self, users, show_all=True):
        pass

    @abstractmethod
    def format_one(self, user):
        pass