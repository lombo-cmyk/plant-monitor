from logging import Logger

from pydantic import BaseModel

from notification.mail.severity import MessageSeverity


class Message(BaseModel):
    receivers: list[str]
    sender: str
    topic: str
    content: str

    @staticmethod
    def build(
        receivers: list[str],
        sender: str,
        topic: str,
        content: str,
        severity: MessageSeverity,
    ) -> "Message":
        topic = severity.value + ": " + topic
        return Message(
            receivers=receivers,
            sender=sender,
            topic=topic,
            content=content,
            severity=severity,
        )


class AbstractMailbox:
    def __init__(self, message: Message, logger: Logger):
        self.logger = logger
        self.message_content = message

    def send(self):
        self._prepare()
        self._send()

    def _prepare(self):
        raise NotImplementedError

    def _send(self):
        raise NotImplementedError
