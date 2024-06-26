import schedule
from time import sleep
from gpiozero import LED

from illumination.logger import logger

    
led = LED(14)


def led_job():
    logger.info(f"Changing led state.")
    led.toggle()


def run():
    schedule.every(10).seconds.do(led_job)
    while True:
        schedule.run_pending()
        sleep(1)