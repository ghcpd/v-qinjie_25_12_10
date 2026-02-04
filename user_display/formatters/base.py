from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    def __init__(self, fields=None):
        self.fields = fields

    @abstractmethod
    def format(self, user):
        pass

    def _select_fields(self, user):
        if not self.fields:
            return user
        return {k: user.get(k) for k in self.fields}

    def format_many(self, users, show_all=True):
        out = []
        for u in users:
            out.append(self.format(u))
        if show_all:
            return "\n".join(out) + "\nPROCESSED=" + str(len(users))
        return "\n".join(out)
