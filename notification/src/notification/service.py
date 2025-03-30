from plant_common.env import config
from plant_common.mqtt.model import EmailContent
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

from notification.mail.manager import MessageManager

RECEIVERS = config["RECEIVERS"]


class Service(BaseService):

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="email/send",
            handler=self.handle_email_send,
            payload_class=EmailContent,
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        pass

    def handle_email_send(self, client: MqttClient, topic: str, message: EmailContent):
        msg = MessageManager(to=RECEIVERS, logger=self.logger, **message.model_dump())
        msg.send()
