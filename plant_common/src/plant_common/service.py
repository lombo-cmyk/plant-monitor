from logging import Logger
from time import sleep

import schedule

from plant_common.mqtt import MqttClient


class BaseService:

    def __init__(self, name: str, logger: Logger, client: MqttClient | None = None):
        self.name = name
        self.logger = logger
        self.client = (
            client
            if client
            else MqttClient(logger, client_id=name, transport="websockets")
        )

    def _subscribe(self, *args, **kwargs):
        raise NotImplementedError

    def _setup_scheduled_jobs(self, *args, **kwargs):
        raise NotImplementedError

    def _pre_run(self, *args, **kwargs):
        """
        Overwrite with any service-specific pre_run code if needed
        """
        pass

    def run(self):
        self.logger.info(f"Starting service {self.name}")

        self._pre_run()
        self._setup_mqtt()
        self._setup_scheduled_jobs()

        while True:
            schedule.run_pending()
            sleep(10)

    def _setup_mqtt(self):
        self.logger.info("Setting up connections")
        self.client.connect(host="mosquitto-broker", port=9001)

        self._subscribe()

        self.client.loop_start()
