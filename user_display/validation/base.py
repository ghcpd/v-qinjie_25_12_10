from abc import ABC, abstractmethod


class ValidationError(Exception):
    pass


class Validator(ABC):
    @abstractmethod
    def validate(self, user):
        pass

    @abstractmethod
    def recover(self, user):
        pass
