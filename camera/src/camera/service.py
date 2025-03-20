from time import sleep

import cv2
import schedule

from plant_common.env import config
from plant_common.model import LedState
from plant_common.mqtt import MqttClient
from plant_common.service import BaseService


class Service(BaseService):

    def _subscribe(self, *args, **kwargs):
        self.client.subscribe(
            topic="led/state", handler=self.handle_led_state, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs):
        schedule.every(10).seconds.do(self.camera_job)

    def handle_led_state(self, client: MqttClient, topic: str, message: LedState):
        if message.state is True:
            self.logger.info("Taking picture")
            sleep(5)  # let camera get the focus
            if config["CAMERA"] is True:  # TODO: temporary
                cam = cv2.VideoCapture(0)
                _, image = cam.read()
                cv2.imwrite("/var/logs/testimage.jpg", image)
                cam.release()

    def camera_job(self):
        self.logger.info("Dummy camera job triggered")
