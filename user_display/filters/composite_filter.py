from .base import BaseFilter


class CompositeFilter(BaseFilter):
    """Loose composite: AND across keys using case-insensitive substring match."""

    def match(self, user, criteria):
        for k, v in criteria.items():
            val = user.get(k, "")
            if isinstance(v, str) and v.startswith("/") and v.endswith("/"):
                # delegate to regex matcher semantics
                from .regex_filter import RegexFilter

                if not RegexFilter().match(user, {k: v}):
                    return False
            else:
                if str(v).lower() not in str(val).lower():
                    return False
        return True
