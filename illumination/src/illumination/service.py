from time import sleep
from threading import Thread

import schedule
from gpiozero import LED

from plant_common.model import LedState
from plant_common.service import BaseService


LED_ON_TIME_S = 15


class Service(BaseService):

    def __init__(self, name, logger, client=None):
        super().__init__(name, logger, client)
        self.led = LED(14)

    def _subscribe(self, *args, **kwargs):
        pass

    def _setup_scheduled_jobs(self, *args, **kwargs):
        schedule.every().hour.at(":01").do(self.led_job)

    def led_job(self):
        self.logger.info(f"Turning LED ON for {LED_ON_TIME_S}s.")
        self.led.on()
        self.client.publish("led/state", LedState.build(True))

        def turn_led_off():
            sleep(LED_ON_TIME_S)
            self.logger.info("Turning LED OFF.")
            self.led.off()
            self.client.publish("led/state", LedState.build(False))

        th = Thread(target=turn_led_off)
        th.start()
