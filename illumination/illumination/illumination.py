from time import sleep     # Import the sleep function from the time module
from gpiozero import LED
import logging
from sys import stdout

logger = logging.getLogger("diodes")

logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

led = LED(14)

def run():
    while True: # Run forever
        led.on()
        logger.info("going through the loop")
        sleep(1)
        led.off()
        sleep(1)