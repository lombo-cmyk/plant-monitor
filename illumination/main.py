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



while True: # Run forever
    led.on()
    logger.info("Loop")
    print("123")
    sleep(1)                  # Sleep for 1 second
    led.off()

    sleep(1)                  # Sleep for 1 second