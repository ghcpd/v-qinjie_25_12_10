from .base import BaseFormatter
from io import StringIO

class CompactFormatter(BaseFormatter):
    def format_many(self, users, show_all=True):
        # Use join and StringIO to minimize allocations
        out = StringIO()
        count = 0
        for u in users:
            out.write(self.format_one(u))
            out.write("\n")
            count += 1
        if show_all:
            out.write(f"PROCESSED={count}\n")
        return out.getvalue().strip()

    def format_one(self, u):
        return (
            f"ID={u.get('id','N/A')} | NAME={u.get('name','')} | EMAIL={u.get('email','')} | ROLE={u.get('role','')} | "
            f"STATUS={u.get('status','')} | JOIN_DATE={u.get('join_date','')} | LAST_LOGIN={u.get('last_login','')}"
        )