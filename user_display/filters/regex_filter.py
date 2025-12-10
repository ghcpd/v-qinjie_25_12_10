import re
from .base import BaseFilter


class RegexFilter(BaseFilter):
    def __init__(self, field, pattern, case_sensitive=False):
        flags = 0 if case_sensitive else re.IGNORECASE
        self.field = field
        self.re = re.compile(pattern, flags)

    def matches(self, user):
        val = user.get(self.field, "")
        if val is None:
            return False
        return bool(self.re.search(str(val)))
