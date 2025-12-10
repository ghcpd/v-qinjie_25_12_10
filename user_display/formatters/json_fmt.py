from .base import BaseFormatter
import json

class JsonFormatter(BaseFormatter):
    def format_many(self, users, show_all=True):
        # return JSON array; attach metadata if show_all
        arr = list(users)
        if show_all:
            return json.dumps({"count": len(arr), "users": arr}, default=str)
        return json.dumps(arr, default=str)

    def format_one(self, u):
        return json.dumps(u, default=str)