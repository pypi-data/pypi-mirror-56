__version__ = '0.0.3'


from .handlers import RabbitMQHandler
from logging import Logger, root
import logging


def getLogger_add_rabbithandler(name=None, level=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    rabbit = RabbitMQHandler(level)
    logger = None
    if name:
        logger = Logger.manager.getLogger(name)
    else:
        logger = root
    logger.setLevel(level)
    logger.addHandler(rabbit)
    return logger


__all__ = ["__version__", "RabbitMQHandler", "getLogger_add_rabbithandler"]
