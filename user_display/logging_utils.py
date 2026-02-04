import logging
import json


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        h.setFormatter(fmt)
        logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger


def struct_log(logger, level, **kwargs):
    msg = json.dumps(kwargs, default=str)
    logger.log(level, msg)
