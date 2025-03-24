from time import sleep

from logging import Logger
import schedule

from plant_common.env import config
from plant_common.model import LedState
from plant_common.mqtt import MqttClient
from plant_common.service import BaseService

from camera.photocamera import Camera
from camera.mock_photocamera import DummyCamera


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
            self.camera.capture()

    def job_read_battery(self) -> None:
        level = self.camera.get_battery_level()

        if level:
            self.latest_battery_level = level
