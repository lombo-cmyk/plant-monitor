from logging import Logger

import boto3

from plant_common.env import config

from notification.mail.abstract_mailbox import AbstractMailbox
from notification.mail.model import Message


class SnsMailbox(AbstractMailbox):

    def __init__(self, message: Message, logger: Logger):
        super().__init__(message, logger)
        self.client = None

    def _prepare(self):
        self.client = boto3.client(
            "sns",
            aws_access_key_id=config["AWS_ACCESS_KEY"],
            aws_secret_access_key=config["AWS_SECRET_KEY"],
            region_name=config["REGION"],
        )

    def _send(self):
        self.client.publish(
            TopicArn=f'arn:aws:sns:{config["REGION"]}:{config["AWS_ACC_ID"]}:RaspberryUniversity',
            Message=self.message_content.content,
            Subject=self.message_content.topic,
        )
