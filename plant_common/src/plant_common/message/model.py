from pydantic import BaseModel

from plant_common.message.severity import Severity


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
        severity: Severity,
    ) -> "Message":
        topic = severity.value + ": " + topic
        return Message(
            receivers=receivers,
            sender=sender,
            topic=topic,
            content=content,
            severity=severity,
        )
