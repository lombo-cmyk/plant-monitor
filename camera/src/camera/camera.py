from functools import partial
from time import sleep

import cv2
import schedule

from plant_common.logger import get_logger
from plant_common.model import LedState
from plant_common.mqtt import MqttClient

logger = get_logger("camera")


def handle_led_state(topic, message):
    if message.state is True:
        logger.info("Taking picture")
        sleep(5)  # let camera get the focus
        cam = cv2.VideoCapture(0)
        _, image = cam.read()
        cv2.imwrite("/var/logs/testimage.jpg", image)
        cam.release()


def camera_job(client: MqttClient):
    pass


def run():
    mqtt_client = MqttClient(client_id="camera", transport="websockets")
    mqtt_client.connect(host="mosquitto-broker", port=9001)
    mqtt_client.subscribe(
        topic="led/state", handler=handle_led_state, payload_class=LedState
    )
    mqtt_client.loop_start()
    fun = partial(camera_job, client=mqtt_client)
    schedule.every(10).seconds.do(fun)
    while True:
        schedule.run_pending()
        sleep(10)
