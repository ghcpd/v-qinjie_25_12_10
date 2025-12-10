from typing import Dict


class BaseFilter:
    def match(self, user: Dict, criteria: Dict) -> bool:
        """Return True if user matches criteria. Subclasses implement behaviour."""
        return True
