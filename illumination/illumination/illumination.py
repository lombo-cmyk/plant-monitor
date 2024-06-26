from time import sleep
from gpiozero import LED

from illumination.logger import logger


led = LED(14)


def run():
    while True:
        led.on()
        logger.info("going through the loop")
        sleep(1)
        led.off()
        sleep(1)