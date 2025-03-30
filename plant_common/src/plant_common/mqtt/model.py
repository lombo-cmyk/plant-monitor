from pydantic import BaseModel

from plant_common.message.severity import Severity


class LedState(BaseModel):
    state: bool

    @staticmethod
    def build(state: bool) -> "LedState":
        return LedState(state=state)


class EmailContent(BaseModel):
    content: str
    topic: str
    severity: Severity

    @staticmethod
    def build(content: str, topic: str, severity=Severity.INFO):
        return EmailContent(content=content, topic=topic, severity=severity)
