from abc import ABC, abstractmethod

class Validator(ABC):
    @abstractmethod
    def validate(self, user):
        """Return a sanitized user dict. May add fallback values."""
        pass