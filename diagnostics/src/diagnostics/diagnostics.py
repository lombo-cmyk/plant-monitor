import logging
import math
from functools import partial
from time import sleep

import schedule
from gpiozero import MCP3008

from diagnostics.mock_devices import MockMCP3008
from plant_common.env import config
from plant_common.logger import get_logger
from plant_common.model import LedState
from plant_common.mqtt import MqttClient

logger = get_logger("diagnostics")
logger.setLevel(logging.WARNING)
led_on = False


def get_thermistor() -> MCP3008:
    if config["THERMISTOR"] is True:
        logger.info("Thermistor present in config. Using real device.")
        return MCP3008(1)
    logger.warning("Thermistor not present in config. Using MOCK")
    return MockMCP3008(1)


def get_photoresistor():
    if config["PHOTORESISTOR"] is True:
        logger.info("hotoresistor present in config. Using real device.")
        return MCP3008(0)
    logger.warning("Photoresistor not present in config. Using MOCK")
    return MockMCP3008(0)


def read_thermistor(thermistor: MCP3008) -> int:
    """
    Read thermistor digital value from 10 bit ADC. Convert it to degree Celsius.
    10k thermistor connected in series with 10k resistor.
    """
    thermistor_digital_value = thermistor.raw_value
    default_temp_k = 25 + 273.15
    beta = 3950
    max_digital_reading = 1023
    try:
        temperature = (
            1
            / (
                1 / default_temp_k
                + math.log(max_digital_reading / thermistor_digital_value - 1) / beta
            )
            - 273.15
        )
    except ZeroDivisionError:
        logger.error("ZeroDivisionError...")
        temperature = 0
    temperature = int(temperature)
    logger.debug(f"Measured temperature is: {temperature}")
    if temperature > 55:
        logger.error(f"Mesured high temperature of {temperature} degree Celcius!!!")
    return temperature


def read_photoresistor(photoresistor: MCP3008):
    """
    Read photoresistor digital value from 10 bit ADC.
    5-10k photoresistor in series with 10k resistor.
    Expected digital values ranging 150-1000 :
    150 - dark room
    500 - dim room
    900 - bright room
    """
    photoresistor_digital_value = photoresistor.raw_value
    DOOR_OPEN_THRESHOLD = 450
    logger.debug(
        f"Measured digital value of photoresistor is {photoresistor_digital_value}"
    )
    if photoresistor_digital_value > DOOR_OPEN_THRESHOLD:
        logger.error("Someone opened the doors...!!!")
    return photoresistor_digital_value


def diagnostics_job(client: MqttClient, thermistor: MCP3008, photoresistor: MCP3008):
    temperature = read_thermistor(thermistor)  # noqa: F841
    brightness = read_photoresistor(photoresistor)  # noqa: F841


def handle_led_state(client: MqttClient, topic: str, message: LedState):
    logger.info(f"Handle led state: {topic}, {message}")


def run():
    thermistor = get_thermistor()
    photoresistor = get_photoresistor()
    mqtt_client = MqttClient(client_id="diagnostics", transport="websockets")
    mqtt_client.connect(host="mosquitto-broker", port=9001)
    mqtt_client.subscribe(
        topic="led/state", handler=handle_led_state, payload_class=LedState
    )
    mqtt_client.loop_start()
    fun = partial(
        diagnostics_job,
        client=None,
        thermistor=thermistor,
        photoresistor=photoresistor,
    )
    schedule.every(10).seconds.do(fun)
    while True:
        schedule.run_pending()
        sleep(10)
