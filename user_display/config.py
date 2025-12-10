import os

class Config:
    # Defaults, can be overridden by env vars
    DEFAULT_FORMAT = os.environ.get("UD_DEFAULT_FORMAT", "compact")
    CACHE_ENABLED = os.environ.get("UD_CACHE_ENABLED", "1") == "1"
    PARALLEL_FILTERING = os.environ.get("UD_PARALLEL_FILTERING", "0") == "1"
    SHARD_COUNT = int(os.environ.get("UD_SHARD_COUNT", "1"))
    METRICS_ENABLED = os.environ.get("UD_METRICS_ENABLED", "1") == "1"
    VALIDATION_STRICT = os.environ.get("UD_VALIDATION_STRICT", "0") == "1"
    MAX_EXPORT_LINES = int(os.environ.get("UD_MAX_EXPORT_LINES", "1000000"))

    @classmethod
    def freeze(cls):
        # prevent runtime changes if needed
        cls._frozen = True


DEFAULT = Config()