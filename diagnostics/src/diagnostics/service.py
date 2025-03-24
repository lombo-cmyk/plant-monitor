import schedule
import math
from logging import Logger
from plant_common.model import LedState
from plant_common.service import BaseService

from gpiozero import MCP3008

from diagnostics.mock_devices import MockMCP3008
from plant_common.env import config
from plant_common.mqtt import MqttClient


class Service(BaseService):

    def __init__(self, name: str, logger: Logger, client: MqttClient | None = None):
        super().__init__(name, logger, client)
        self.thermistor = self.get_thermistor()
        self.photoresistor = self.get_photoresistor()

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="led/state", handler=self.handle_led_state, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every(10).seconds.do(self.diagnostics_job)

    def handle_led_state(
        self, client: MqttClient, topic: str, message: LedState
    ) -> None:
        self.logger.info(f"Handle led state: {topic}, {message}")

    def diagnostics_job(self) -> None:
        temperature = self.read_thermistor()  # noqa: F841
        brightness = self.read_photoresistor()  # noqa: F841

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
        temperature = int(temperature)
        self.logger.debug(f"Measured temperature is: {temperature}")
        if temperature > 55:
            self.logger.error(
                f"Mesured high temperature of {temperature} degree Celcius!!!"
            )
        return temperature

    def read_photoresistor(self) -> int:
        """
        Read photoresistor digital value from 10 bit ADC.
        5-10k photoresistor in series with 10k resistor.
        Expected digital values ranging 150-1000 :
        150 - dark room
        500 - dim room
        900 - bright room
        """
        photoresistor_digital_value = self.photoresistor.raw_value
        DOOR_OPEN_THRESHOLD = 450
        self.logger.debug(
            f"Measured digital value of photoresistor is {photoresistor_digital_value}"
        )
        if photoresistor_digital_value > DOOR_OPEN_THRESHOLD:
            self.logger.error("Someone opened the doors...!!!")
        return photoresistor_digital_value
