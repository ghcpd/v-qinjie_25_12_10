import os

DEFAULTS = {
    "parallel_filtering": False,
    "shard_size": 512,
}

# Allow environment overrides
for k in list(DEFAULTS.keys()):
    env = os.getenv(f"USER_DISPLAY_{k.upper()}")
    if env is not None:
        DEFAULTS[k] = type(DEFAULTS[k])(env)
