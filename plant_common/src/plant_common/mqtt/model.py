from datetime import datetime, timedelta

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


class EventDetails(BaseModel):
    duration: timedelta
    start: datetime
    stop: datetime

    @staticmethod
    def build(duration: timedelta, start: datetime, stop: datetime) -> "EventDetails":
        return EventDetails(duration=duration, start=start, stop=stop)

    def __str__(self):
        return f"\n    - Started: {self.start}. Stopped: {self.stop}. Duration: {self.duration}"


class NotificationCollector(BaseModel):
    high_temperature: EventDetails | None = None
    high_light: EventDetails | None = None
    picture_path: str | None = None
    uptime: dict[str, timedelta] | None = None
