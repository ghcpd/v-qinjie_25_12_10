import json
from .base import BaseFormatter


class JSONFormatter(BaseFormatter):
    def format(self, user):
        u = self._select_fields(user)
        return json.dumps(u, ensure_ascii=False)
