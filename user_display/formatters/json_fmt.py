import json
from .base import Formatter


class JsonFormatter(Formatter):
    def format_many(self, users, show_all=True, export=False):
        # Avoid repeated parsing; dump once
        data = list(users)
        return json.dumps({"users": data, "count": len(data)}, default=str)

    def format_one(self, user):
        return json.dumps(user, default=str)
