from logging import Logger

from plant_common.env import config

from notification.mail.abstract_mailbox import AbstractMailbox, Message
from notification.mail.gmail.mailbox import GmailMailbox
from notification.mail.severity import MessageSeverity

SENDER = config["SENDER"]
MAILBOX = config["MAILBOX"]

MAILBOX_CLS = {"GMAIL": GmailMailbox}


class MessageManager:

    def __init__(
        self,
        to: list[str],
        topic: str,
        content: str,
        severity: MessageSeverity,
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
