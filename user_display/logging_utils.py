import logging
import json

_logger = logging.getLogger("user_display")
_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.INFO)


def get_logger(name=None):
    if name:
        return logging.getLogger(f"user_display.{name}")
    return _logger


def struct_log(level, msg, **kwargs):
    # Structured log as JSON in message to remain compatible with stdout
    logger = get_logger()
    text = msg + " | " + json.dumps(kwargs, default=str)
    if level == "info":
        logger.info(text)
    elif level == "debug":
        logger.debug(text)
    elif level == "warn":
        logger.warning(text)
    elif level == "error":
        logger.error(text)
    else:
        logger.info(text)