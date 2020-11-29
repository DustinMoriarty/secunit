import os

from logging import INFO
from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from sys import stderr


def saturate(value, min, max):
    if value < min:
        return min
    if value > max:
        return max
    return value


def default_logger(name, level=INFO):
    env_level = os.getenv("SECUNIT_LOG_LEVEL")
    if env_level is not None:
        level = env_level
    logger = getLogger(name)
    logger.setLevel(level)
    sh = StreamHandler(stderr)
    sh.setLevel(level)
    logger.addHandler(sh)
    fmt = Formatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")
    sh.setFormatter(fmt)
    return logger


APP_NAME = __package__
