import logging
from sys import stdout

logger = logging.getLogger("diodes")

logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
fileHandler = logging.FileHandler(filename="/var/logs/diodes.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)