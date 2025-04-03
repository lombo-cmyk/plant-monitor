from logging import Logger

import schedule
from gpiozero import LED

from plant_common.message.severity import Severity
from plant_common.mqtt.model import EmailContent, LedState
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService
from plant_common.utils.timer import Timer


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

    def _subscribe(self, *args, **kwargs) -> None:
        super()._subscribe(*args, **kwargs)
        self.client.subscribe(topic="led/off", handler=self.handle_led_off)

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every().hour.at(":01").do(self.led_on_job)

    def led_on_job(self) -> None:
        if not self.led:
            if not self._pre_run():
                return

        self.logger.info("Turning LED ON for the camera.")
        self.led.on()
        self.client.publish("led/state", LedState.build(True))

    def handle_led_off(self, client: MqttClient, topic: str, message: str):
        if not self.led:
            if not self._pre_run():
                return

        self.logger.info("Turning LED OFF.")
        self.led.off()
        self.client.publish("led/state", LedState.build(False))

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
