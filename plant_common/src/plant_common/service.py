import signal
from logging import Logger
from time import sleep

import schedule

from plant_common.mqtt.mqtt import MqttClient


class BaseService:

    def __init__(
        self, name: str, logger: Logger, client: MqttClient | None = None
    ) -> None:
        self.name = name
        self.logger = logger
        self.client = (
            client
            if client
            else MqttClient(logger, client_id=name, transport="websockets")
        )
        self.shutdown = False

        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _subscribe(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def _pre_run(self, *args, **kwargs) -> None:
        """
        Overwrite with any service-specific pre_run code if needed
        """
        pass

    def _shutdown(self, signum, frame) -> None:
        self.logger.debug("Shutting down.")
        schedule.clear()
        self.client.disconnect()
        self.shutdown = True
        self.logger.info("Shutdown complete.")

    def _setup_mqtt(self) -> None:
        self.logger.info("Setting up connections")
        self.client.connect(host="mosquitto-broker", port=9001)

        self._subscribe()

        self.client.loop_start()

    def run(self) -> None:
        """
        Main service loop. Runs forever.
        """
        self.logger.info(f"Starting service {self.name}")

        self._setup_mqtt()

        self._pre_run()

        self._setup_scheduled_jobs()

        while True:
            schedule.run_pending()

            if self.shutdown:
                break

            sleep(1)
