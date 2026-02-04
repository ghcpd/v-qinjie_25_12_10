from .base import Formatter


class CompactFormatter(Formatter):
    def format(self, user):
        parts = [
            f"ID={user.get('id','N/A')}",
            f"NAME={user.get('name','')}",
            f"EMAIL={user.get('email','')}",
        ]
        return " | ".join(parts)

    def header(self):
        return "COMPACT_EXPORT_BEGIN"

    def footer(self):
        return "COMPACT_EXPORT_END"
