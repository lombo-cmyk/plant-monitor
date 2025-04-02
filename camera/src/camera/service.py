from logging import Logger
from time import sleep

import gphoto2 as gp

from plant_common.env import config
from plant_common.message.severity import Severity
from plant_common.mqtt.model import EmailContent, LedState, NotificationCollector
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService
from plant_common.utils.timer import Timer

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
        self.camera_error_alert_timer = Timer(3600, self.dummy_timer)

    def _pre_run(self, *args, **kwargs) -> None:
        try:
            self.camera.set_capture_target()
            self.camera.get_battery_level()
        except gp.GPhoto2Error as e:
            self.handle_camera_error(
                msg="Camera exception while connecting to camera",
                topic="Couldn't connect to camera",
                exc=e,
            )
            return
        except Exception as e:
            self.handle_camera_error(
                msg="Unknown exception while connecting to camera",
                topic="Unknown exception while using camera",
                exc=e,
            )
            return

    def _subscribe(self, *args, **kwargs) -> None:
        super()._subscribe(*args, **kwargs)
        self.client.subscribe(
            topic="led/state", handler=self.handle_make_picture, payload_class=LedState
        )

    def _setup_scheduled_jobs(self, *args, **kwargs):
        pass

    def handle_make_picture(
        self, client: MqttClient, topic: str, message: LedState
    ) -> None:
        if message.state is False:
            return

        self.logger.info("Taking picture")
        sleep(3)  # let camera get the focus after light is turned on
        try:
            filename = self.camera.capture()
        except gp.GPhoto2Error as e:
            self.handle_camera_error(
                msg="Exception while taking photo", topic="Couldn't take photo", exc=e
            )
            return
        except Exception as e:
            self.handle_camera_error(
                msg="Unknown exception while taking photo",
                topic="Unknown exception while using camera",
                exc=e,
            )
            return

        notification = NotificationCollector(picture_path=filename)
        self.client.publish("notification/gather", notification)

    def handle_camera_error(self, msg, topic, exc):
        self.logger.exception(msg)
        if not self.camera_error_alert_timer.is_counting():
            self.camera_error_alert_timer.reset()
            self.camera_error_alert_timer.start()
            msg = EmailContent.build(
                content=f"{msg}: {exc}", topic=topic, severity=Severity.ERROR
            )
            self.client.publish("email/send", msg)

    def dummy_timer(self):
        pass
