from .base import BaseFormatter


class CompactFormatter(BaseFormatter):
    def format(self, user):
        u = self._select_fields(user)
        parts = []
        if "id" in u:
            parts.append(f"ID={u.get('id')}")
        if "name" in u:
            parts.append(f"NAME={u.get('name')}")
        if "email" in u:
            parts.append(f"EMAIL={u.get('email')}")
        if "role" in u:
            parts.append(f"ROLE={u.get('role')}")
        if "status" in u:
            parts.append(f"STATUS={u.get('status')}")
        return " | ".join(parts)
