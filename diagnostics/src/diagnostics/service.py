import math
from datetime import datetime
from logging import Logger

import schedule
from gpiozero import MCP3008

from plant_common.env import config
from plant_common.message.severity import Severity
from plant_common.mqtt.model import (
    EmailContent,
    EventDetails,
    LedState,
    NotificationCollector,
)
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

from diagnostics.mock_devices import MockMCP3008
from diagnostics.utils.timer import Timer


class Service(BaseService):
    DOOR_OPEN_THRESHOLD = 450
    TEMP_WARN_THRESHOLD = 40
    TEMP_ERROR_THRESHOLD = 60

    def __init__(self, name: str, logger: Logger, client: MqttClient | None = None):
        super().__init__(name, logger, client)
        self.thermistor = self.get_thermistor()
        self.photoresistor = self.get_photoresistor()
        self.is_led_on = False
        self.light_alert_start: datetime | None = None
        self.temp_warn_alert_start: datetime | None = None

        # Send error temperature alerts not more often than Timer's wait_time
        self.temp_error_alert_timer = Timer(3600, self.dummy_timer)

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="led/state", handler=self.handle_led_state, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every(10).seconds.do(self.diagnostics_job)

    def handle_led_state(
        self, client: MqttClient, topic: str, message: LedState
    ) -> None:
        self.is_led_on = message.state

    def diagnostics_job(self) -> None:
        temperature = self.read_thermistor()  # noqa: F841
        brightness = self.read_photoresistor()  # noqa: F841

        self.evaluate_temperature(temperature)

        if self.is_led_on:
            return
        self.evaluate_brightness(brightness)

    def evaluate_temperature(self, temperature: int):
        if temperature > self.TEMP_ERROR_THRESHOLD:
            self.logger.error(
                f"Mesured high temperature of {temperature} degree Celcius!"
            )
            if not self.temp_error_alert_timer.is_counting():
                self.temp_error_alert_timer.reset()
                self.temp_error_alert_timer.start()

                msg = f"Detected high temperature of LEDs.\n\nMeasured {temperature}°C.\n\nAction required!"
                topic = "High temperature detected"
                mail = EmailContent.build(
                    content=msg, topic=topic, severity=Severity.ERROR
                )
                self.client.publish("email/send", mail)

        elif temperature > self.TEMP_WARN_THRESHOLD and not self.temp_warn_alert_start:
            self.logger.warning(
                f"Mesured high temperature of {temperature} degree Celcius!"
            )
            self.temp_warn_alert_start = datetime.now().replace(microsecond=0)

        elif temperature < self.TEMP_WARN_THRESHOLD and self.temp_warn_alert_start:
            now = datetime.now().replace(microsecond=0)
            duration = now - self.temp_warn_alert_start
            self.logger.warning(f"Temperature was high for {duration}, but now is OK")

            event = EventDetails.build(
                duration=duration, start=self.temp_warn_alert_start, stop=now
            )
            msg = NotificationCollector(high_temperature=event)
            self.client.publish("notification/gather", msg)

            self.temp_warn_alert_start = None

        elif temperature > self.TEMP_WARN_THRESHOLD and self.temp_warn_alert_start:
            self.logger.debug("Light intensity still too high...")

    def evaluate_brightness(self, brightness):
        if brightness > self.DOOR_OPEN_THRESHOLD and not self.light_alert_start:
            self.logger.warning("Light intensity too high!")
            self.light_alert_start = datetime.now().replace(microsecond=0)

        elif brightness < self.DOOR_OPEN_THRESHOLD and self.light_alert_start:
            now = datetime.now().replace(microsecond=0)
            duration = now - self.light_alert_start
            self.logger.warning(
                f"Light intensity was high for {duration}, but now is OK"
            )

            event = EventDetails.build(
                duration=duration, start=self.light_alert_start, stop=now
            )
            msg = NotificationCollector(high_light=event)
            self.client.publish("notification/gather", msg)

            self.light_alert_start = None

        elif brightness > self.DOOR_OPEN_THRESHOLD and self.light_alert_start:
            self.logger.debug("Light intensity still too high...")

    def get_thermistor(self) -> MCP3008:
        if config["THERMISTOR"] is True:
            self.logger.info("Thermistor present in config. Using real device.")
            return MCP3008(1)
        self.logger.warning("Thermistor not present in config. Using MOCK")
        return MockMCP3008(1)

    def get_photoresistor(self) -> MCP3008:
        if config["PHOTORESISTOR"] is True:
            self.logger.info("hotoresistor present in config. Using real device.")
            return MCP3008(0)
        self.logger.warning("Photoresistor not present in config. Using MOCK")
        return MockMCP3008(0)

    def read_thermistor(self) -> int:
        """
        Read thermistor digital value from 10 bit ADC. Convert it to degree Celsius.
        10k thermistor connected in series with 10k resistor.
        """
        thermistor_digital_value = self.thermistor.raw_value
        default_temp_k = 25 + 273.15
        beta = 3950
        max_digital_reading = 1023
        try:
            temperature = (
                1
                / (
                    1 / default_temp_k
                    + math.log(max_digital_reading / thermistor_digital_value - 1)
                    / beta
                )
                - 273.15
            )
        except ZeroDivisionError:
            self.logger.error("ZeroDivisionError...")
            temperature = 0

        return int(temperature)

    def read_photoresistor(self) -> int:
        """
        Read photoresistor digital value from 10 bit ADC.
        5-10k photoresistor in series with 10k resistor.
        Expected digital values ranging 150-1000 :
        150 - dark room
        500 - dim room
        900 - bright room
        """
        return self.photoresistor.raw_value

    def dummy_timer():
        pass
