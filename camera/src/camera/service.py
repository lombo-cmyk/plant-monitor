from time import sleep
from threading import Lock

import schedule

from plant_common.env import config
from plant_common.model import LedState
from plant_common.mqtt import MqttClient
from plant_common.service import BaseService

from camera.photocamera import Camera


class Service(BaseService):

    def __init__(self, name, logger, client=None):
        super().__init__(name, logger, client)
        self.mutex = Lock()
        self.latest_battery_level = None  # TODO: will be used for e-mailing,
        # needs a timestamp {"ts": ..., "level": ...}

    def _pre_run(self, *args, **kwargs):
        with self.mutex:
            if config["CAMERA"] is True:
                camera = Camera(self.logger)
                camera.set_capture_target()
                camera.get_battery_level()
                camera.exit()

    def _subscribe(self, *args, **kwargs):
        self.client.subscribe(
            topic="led/state", handler=self.handle_led_state, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs):
        schedule.every(30).minutes.do(self.job_read_battery)

    def handle_led_state(self, client: MqttClient, topic: str, message: LedState):
        if message.state is True:
            self.logger.info("Taking picture")
            sleep(5)  # let camera get the focus after light is turned on
            with self.mutex:
                if config["CAMERA"] is True:
                    camera = Camera(self.logger)
                    camera.capture()
                    camera.exit()

    def job_read_battery(self):
        level = None
        with self.mutex:
            if config["CAMERA"] is True:
                camera = Camera(self.logger)
                level = camera.get_battery_level()
                camera.exit()

        if level:
            self.latest_battery_level = level
