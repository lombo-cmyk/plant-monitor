from logging import Logger
from time import sleep

import schedule

from plant_common.env import config
from plant_common.mqtt.model import LedState, NotificationCollector
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

from camera.mock_photocamera import DummyCamera
from camera.photocamera import Camera


class Service(BaseService):

    def __init__(self, name: str, logger: Logger, client: MqttClient | None = None):
        super().__init__(name, logger, client)
        self.camera = (
            Camera(self.logger)
            if config["CAMERA"] is True
            else DummyCamera(self.logger)
        )
        self.latest_battery_level = None  # TODO: will be used for e-mailing,
        # needs a timestamp {"ts": ..., "level": ...}

    def _pre_run(self, *args, **kwargs) -> None:
        self.camera.set_capture_target()
        self.camera.get_battery_level()

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="led/state", handler=self.handle_make_picture, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every(config["BATTERY_READ_INTERVAL_M"]).minutes.do(
            self.job_read_battery
        )

    def handle_make_picture(
        self, client: MqttClient, topic: str, message: LedState
    ) -> None:
        if message.state is True:
            self.logger.info("Taking picture")
            sleep(5)  # let camera get the focus after light is turned on
            filename = self.camera.capture()
            notification = NotificationCollector(picture_path=filename)
            self.client.publish("notification/gather", notification)

    def job_read_battery(self) -> None:
        level = self.camera.get_battery_level()

        if level:
            self.latest_battery_level = level
