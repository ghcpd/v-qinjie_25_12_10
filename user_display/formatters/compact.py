from io import StringIO
from .base import Formatter


class CompactFormatter(Formatter):
    def format_many(self, users, show_all=True, export=False):
        buf = StringIO()
        for u in users:
            buf.write(self.format_one(u) + "\n")
        if show_all:
            buf.write(f"PROCESSED={len(users)}\n")
        return buf.getvalue()

    def format_one(self, user):
        parts = [
            f"ID={user.get('id','N/A')}",
            f"NAME={user.get('name','')}",
            f"EMAIL={user.get('email','')}",
            f"ROLE={user.get('role','')}",
            f"STATUS={user.get('status','')}",
        ]
        return " | ".join(parts)
