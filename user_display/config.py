import os


class Config:
    def __init__(self, **kwargs):
        self._frozen = False
        self.values = {
            "max_workers": int(os.environ.get("UD_MAX_WORKERS", "4")),
            "cache_enabled": True,
        }
        self.values.update(kwargs)

    def get(self, key, default=None):
        return self.values.get(key, default)

    def set(self, key, value):
        if self._frozen:
            raise RuntimeError("Config is frozen")
        self.values[key] = value

    def freeze(self):
        self._frozen = True
