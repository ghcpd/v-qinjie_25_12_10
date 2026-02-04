import re
from .base import BaseFilter

class RegexFilter(BaseFilter):
    def __init__(self, field, pattern, flags=0):
        self.field = field
        self.regex = re.compile(pattern, flags)

    def match(self, user):
        v = user.get(self.field, "")
        if v is None:
            return False
        return bool(self.regex.search(str(v)))