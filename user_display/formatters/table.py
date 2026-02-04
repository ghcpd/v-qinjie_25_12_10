from .base import BaseFormatter


class TableFormatter(BaseFormatter):
    def format(self, user):
        u = self._select_fields(user)
        parts = []
        for k, v in u.items():
            parts.append(f"{k}: {v}")
        return "\n".join(parts)
