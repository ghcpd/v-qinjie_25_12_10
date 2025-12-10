from io import StringIO
from .base import Formatter


class TableFormatter(Formatter):
    def format_many(self, users, show_all=True, export=False):
        buf = StringIO()
        buf.write("EXPORT_BEGIN\n")
        buf.write("=" * 80 + "\n")
        for u in users:
            buf.write(self.format_one(u) + "\n")
            buf.write("-" * 80 + "\n")
        buf.write("EXPORT_END\n")
        return buf.getvalue()

    def format_one(self, user):
        return f"UserID: {user.get('id','N/A')}\n  Name: {user.get('name','')}\n  Email: {user.get('email','') }"
