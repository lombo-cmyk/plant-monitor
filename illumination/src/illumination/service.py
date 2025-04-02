from logging import Logger
from threading import Thread
from time import sleep

import schedule
from gpiozero import LED

from plant_common.message.severity import Severity
from plant_common.mqtt.model import EmailContent, LedState
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService
from plant_common.utils.timer import Timer

LED_ON_TIME_S = 15


class Service(BaseService):

    def __init__(
        self, name: str, logger: Logger, client: MqttClient | None = None
    ) -> None:
        super().__init__(name, logger, client)
        self.led = None
        self.led_error_alert_timer = Timer(3600, self.dummy_timer)

    def _pre_run(self, *args, **kwargs):
        try:
            self.led = LED(14)
            self.led.on()
            self.led.off()
        except Exception as e:
            self.led = None
            self.handle_peripheral_error(
                msg="Can't connect LED driver", topic="LED error", exc=e
            )
            return False
        return True

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every().hour.at(":01").do(self.led_job)

    def led_job(self) -> None:
        if not self.led:
            if not self._pre_run():
                return

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

    def handle_peripheral_error(self, msg, topic, exc):
        self.logger.exception(msg)
        if not self.led_error_alert_timer.is_counting():
            self.led_error_alert_timer.reset()
            self.led_error_alert_timer.start()
            msg = EmailContent.build(
                content=f"{msg}: {exc}", topic=topic, severity=Severity.ERROR
            )
            self.client.publish("email/send", msg)

    def dummy_timer():
        pass
