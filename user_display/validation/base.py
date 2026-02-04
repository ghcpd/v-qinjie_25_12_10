from abc import ABC, abstractmethod
from typing import Dict


class Validator(ABC):
    @abstractmethod
    def validate(self, user: Dict) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    def recover(self, user: Dict) -> Dict:
        raise NotImplementedError()
