from logging import Logger

from plant_common.env import config
from plant_common.message.model import Message
from plant_common.message.severity import Severity

from notification.mail.abstract_mailbox import AbstractMailbox
from notification.mail.gmail.mailbox import GmailMailbox

SENDER = config["SENDER"]
MAILBOX = config["MAILBOX"]

MAILBOX_CLS = {"GMAIL": GmailMailbox}


class MessageManager:

    def __init__(
        self,
        to: list[str],
        topic: str,
        content: str,
        severity: Severity,
        logger: Logger,
    ):
        self.message = Message.build(
            receivers=to, sender=SENDER, topic=topic, content=content, severity=severity
        )
        self.logger = logger

    def send(self):
        MailboxCls: AbstractMailbox = MAILBOX_CLS[MAILBOX]
        mailbox = MailboxCls(self.message, self.logger)
        mailbox.send()
