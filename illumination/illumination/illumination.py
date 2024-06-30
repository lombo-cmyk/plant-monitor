import schedule
from time import sleep
from gpiozero import LED
from paho.mqtt.client import Client
from functools import partial
from typing import Optional
from illumination.logger import logger
from illumination.model import LedState
from threading import Thread

led = LED(14)
LED_ON_TIME_S = 5

def led_job(client: Client):
    logger.info(f"Turning LED ON.")
    led.on()
    client.publish("led/state", payload=LedState.build(True).model_dump_json())

    def turn_led_off():
        sleep(LED_ON_TIME_S)
        logger.info(f"Turning LED OFF.")
        led.off()
        client.publish("led/state", payload=LedState.build(False).model_dump_json())
    th = Thread(target=turn_led_off)
    th.start()


def run():
    mqtt_client = Client(client_id="illumination", transport="websockets")
    mqtt_client.connect(host="mosquitto-broker", port=9001)
    fun = partial(led_job, client=mqtt_client)
    schedule.every(10).seconds.do(fun)
    while True:
        schedule.run_pending()
        sleep(1)