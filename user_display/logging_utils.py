import logging
import json


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        h.setFormatter(fmt)
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger


def structured_log(logger, level, msg, **kwargs):
    entry = {"message": msg, **kwargs}
    logger.log(level, json.dumps(entry))
    return entry
