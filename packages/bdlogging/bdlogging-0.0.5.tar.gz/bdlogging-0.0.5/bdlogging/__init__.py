__version__ = '0.0.5'


from .handlers import RabbitMQHandler, get_logging_level
from logging import Logger, root
import logging
import time


def getLogger_add_rabbithandler(name=None, level=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    cnt = 0
    if not level:
        level = get_logging_level()
    rabbit: RabbitMQHandler = None
    while True:
        try:
            rabbit = RabbitMQHandler(level)
            break
        except Exception as ex:
            if cnt > 10:
                raise ex
            time.sleep(5)
            cnt += 1

    logger = None
    if name:
        logger = Logger.manager.getLogger(name)
    else:
        logger = root
    logger.setLevel(level)
    logger.addHandler(rabbit)
    return logger


__all__ = ["__version__", "RabbitMQHandler", "getLogger_add_rabbithandler"]
