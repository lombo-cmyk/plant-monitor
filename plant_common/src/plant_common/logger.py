import logging
from sys import stdout


def get_logger(name: str):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter(
        "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"
    )
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler(filename=f"/var/logs/{name}.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)
    return logger
