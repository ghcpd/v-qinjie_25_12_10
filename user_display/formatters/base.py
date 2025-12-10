from abc import ABC, abstractmethod
from typing import Dict


class Formatter(ABC):
    """Base formatter interface."""

    @abstractmethod
    def format(self, user: Dict) -> str:
        raise NotImplementedError()

    def header(self) -> str:
        return ""

    def footer(self) -> str:
        return ""

    def export(self, user: Dict) -> str:
        # default export is same as line format
        return self.format(user)
