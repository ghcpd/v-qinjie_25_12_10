import os

class Config:
    DEFAULTS = {
        "formatter": os.environ.get("UD_FORMATTER", "compact"),
        "filter_parallel": os.environ.get("UD_FILTER_PARALLEL", "false").lower() in ("1","true","yes"),
        "max_cache": int(os.environ.get("UD_MAX_CACHE", "4096")),
    }

    @classmethod
    def get(cls, k, default=None):
        return cls.DEFAULTS.get(k, default)
