import re
from .base import BaseFilter


class RegexFilter(BaseFilter):
    def match(self, user, criteria):
        # If a criteria value starts and ends with / treat as regex
        for k, v in criteria.items():
            val = user.get(k, "")
            if isinstance(v, str) and len(v) >= 2 and v.startswith("/") and v.endswith("/"):
                try:
                    rx = re.compile(v.strip("/"))
                    if not rx.search(str(val)):
                        return False
                except re.error:
                    return False
            else:
                # fallback to substring (case-insensitive)
                if str(v).lower() not in str(val).lower():
                    return False
        return True
