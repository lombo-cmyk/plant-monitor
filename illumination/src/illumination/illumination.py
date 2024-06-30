from functools import partial
from threading import Thread
from time import sleep

import schedule
from gpiozero import LED

from plant_common.logger import get_logger
from plant_common.model import LedState
from plant_common.mqtt import MqttClient

logger = get_logger("illumination")
led = LED(14)
LED_ON_TIME_S = 5


def led_job(client: MqttClient):
    logger.info("Turning LED ON.")
    led.on()
    client.publish("led/state", LedState.build(True))

    def turn_led_off():
        sleep(LED_ON_TIME_S)
        logger.info("Turning LED OFF.")
        led.off()
        client.publish("led/state", LedState.build(False))

    th = Thread(target=turn_led_off)
    th.start()


def run():
    mqtt_client = MqttClient(client_id="illumination", transport="websockets")
    mqtt_client.connect(host="mosquitto-broker", port=9001)
    fun = partial(led_job, client=mqtt_client)
    schedule.every(10).seconds.do(fun)
    while True:
        schedule.run_pending()
        sleep(1)
