import schedule
from jinja2 import Environment, FileSystemLoader

from plant_common.env import config
from plant_common.message.severity import Severity
from plant_common.mqtt.model import EmailContent, NotificationCollector
from plant_common.mqtt.mqtt import MqttClient
from plant_common.service import BaseService

from notification.mail.manager import MessageManager
from notification.utils.notification_center import NotificationCenter


class Service(BaseService):

    def __init__(self, name, logger, client=None):
        super().__init__(name, logger, client)
        self.gethered_notifications = NotificationCenter()

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

        if config["MAILBOX"] == "MOCK":
            self.logger.warning("Runnign with MOCKED mailbox.")

    def _subscribe(self, *args, **kwargs) -> None:
        self.client.subscribe(
            topic="email/send",
            handler=self.handle_email_send,
            payload_class=EmailContent,
        )
        self.client.subscribe(
            topic="notification/gather",
            handler=self.handle_notification_gather,
            payload_class=NotificationCollector,
        )

    def _setup_scheduled_jobs(self, *args, **kwargs) -> None:
        schedule.every().day.at("09:00").do(self.send_summary)

    def send_summary(self):
        self.logger.debug("Sending notification summary")
        environment = Environment(
            loader=FileSystemLoader("/usr/src/app/template"), trim_blocks=True
        )
        template = environment.get_template("summary.jinja2")

        intense_light = "".join(map(str, self.gethered_notifications.high_light))
        high_temp = "".join(map(str, self.gethered_notifications.high_temperature))
        pictures = ", ".join(self.gethered_notifications.pictures)

        content = template.render(
            intense_light=intense_light, high_temp=high_temp, pictures=pictures
        )
        topic = "Daily Raspberry summary"
        msg = MessageManager(
            to=config.get("RECEIVERS", ""),
            topic=topic,
            content=content,
            severity=Severity.INFO,
            logger=self.logger,
        )
        msg.send()

        self.gethered_notifications = NotificationCenter()

    def handle_email_send(self, client: MqttClient, topic: str, message: EmailContent):
        msg = MessageManager(
            to=config.get("RECEIVERS", ""), logger=self.logger, **message.model_dump()
        )
        msg.send()

    def handle_notification_gather(
        self, client: MqttClient, topic: str, message: EmailContent
    ):
        self.gethered_notifications.update(message)
