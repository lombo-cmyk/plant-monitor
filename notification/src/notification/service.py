from plant_common.env import config
from plant_common.mqtt.model import EmailContent
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

from notification.mail.manager import MessageManager


class Service(BaseService):

    def _pre_run(self, *args, **kwargs):
        is_gmail_error = config["MAILBOX"] == "GMAIL" and not all(
            [config.get("SENDER"), config.get("RECEIVERS")]
        )
        is_sns_error = config["MAILBOX"] == "SNS" and not all(
            [
                config.get("AWS_ACCESS_KEY"),
                config.get("AWS_SECRET_KEY"),
                config.get("REGION"),
                config.get("AWS_ACC_ID"),
            ]
        )
        if is_gmail_error or is_sns_error:
            self.logger.error("Wrong mailbox configuration. See Readme.")
            exit(1)

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="email/send",
            handler=self.handle_email_send,
            payload_class=EmailContent,
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        pass

    def handle_email_send(self, client: MqttClient, topic: str, message: EmailContent):
        msg = MessageManager(
            to=config.get("RECEIVERS", ""), logger=self.logger, **message.model_dump()
        )
        msg.send()
