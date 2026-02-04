import json
from .base import Formatter


class JSONFormatter(Formatter):
    def format(self, user):
        return json.dumps(user, default=str, separators=(",",":"))

    def header(self):
        return "["

    def footer(self):
        return "]"

    def export(self, user):
        return json.dumps(user, default=str)
