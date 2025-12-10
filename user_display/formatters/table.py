from .base import BaseFormatter
from io import StringIO

class TableFormatter(BaseFormatter):
    def format_many(self, users, show_all=True):
        # produce a simple ASCII table
        if not users:
            return "(no users)"
        headers = ["ID", "NAME", "EMAIL", "ROLE", "STATUS", "JOIN_DATE", "LAST_LOGIN"]
        widths = {h: len(h) for h in headers}
        rows = []
        for u in users:
            row = [str(u.get('id','')), u.get('name',''), u.get('email',''), u.get('role',''), u.get('status',''), u.get('join_date',''), u.get('last_login','')]
            rows.append(row)
            for h, cell in zip(headers, row):
                widths[h] = max(widths[h], len(str(cell)))
        out = StringIO()
        sep = "+" + "+".join(["-" * (widths[h] + 2) for h in headers]) + "+\n"
        out.write(sep)
        out.write("| " + " | ".join(h.ljust(widths[h]) for h in headers) + " |\n")
        out.write(sep)
        for row in rows:
            out.write("| " + " | ".join(str(cell).ljust(widths[h]) for h, cell in zip(headers, row)) + " |\n")
        out.write(sep)
        if show_all:
            out.write(f"PROCESSED={len(rows)}\n")
        return out.getvalue()

    def format_one(self, u):
        # single-row table
        return self.format_many([u], show_all=False)