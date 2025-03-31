from logging import Logger
from threading import Thread
from time import sleep

import schedule
from gpiozero import LED

from plant_common.mqtt.model import LedState
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

LED_ON_TIME_S = 15


class Service(BaseService):

    def __init__(
        self, name: str, logger: Logger, client: MqttClient | None = None
    ) -> None:
        super().__init__(name, logger, client)
        self.led = LED(14)

    def _subscribe(self, *args, **kwargs) -> None:
        pass

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every().hour.at(":01").do(self.led_job)

    def led_job(self) -> None:
        self.logger.info(f"Turning LED ON for {LED_ON_TIME_S}s.")
        self.led.on()
        self.client.publish("led/state", LedState.build(True))

        def turn_led_off() -> None:
            sleep(LED_ON_TIME_S)
            self.logger.info("Turning LED OFF.")
            self.led.off()
            self.client.publish("led/state", LedState.build(False))

        th = Thread(target=turn_led_off)
        th.start()
