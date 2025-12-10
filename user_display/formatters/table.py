from .base import Formatter


class TableFormatter(Formatter):
    def format(self, user):
        # Quick single-line table-ish representation
        return f"UserID: {user.get('id','N/A')} | Name: {user.get('name','')} | Email: {user.get('email','')}"

    def header(self):
        return "EXPORT_BEGIN\n" + ("-" * 80)

    def footer(self):
        return "EXPORT_END"

    def export(self, user):
        parts = [
            f"UserID: {user.get('id','N/A')}",
            f"  Name: {user.get('name','')}",
            f"  LastLogin: {user.get('last_login','')}",
            "-" * 40,
        ]
        return "\n".join(parts)
