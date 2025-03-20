import logging
import logging.handlers
from sys import stdout


def get_logger(name: str):

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter(
        "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
    )
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)

    timedRotatingHandler = logging.handlers.TimedRotatingFileHandler(
        filename=f"/var/logs/{name}.log", when="D", interval=7, backupCount=4
    )
    timedRotatingHandler.setFormatter(logFormatter)

    timedRotatingHandler.doRollover()

    logger.addHandler(timedRotatingHandler)
    logger.addHandler(consoleHandler)

    return logger
