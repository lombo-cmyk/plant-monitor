from datetime import timedelta

from pydantic import BaseModel

from plant_common.mqtt.model import EventDetails, NotificationCollector


class NotificationCenter(BaseModel):
    high_temperature: list[EventDetails] = []
    high_light: list[EventDetails] = []
    pictures: list[str] = []
    uptimes: dict[str, timedelta] = {}

    def update(self, data: NotificationCollector):
        if data.high_temperature:
            self.high_temperature.append(data.high_temperature)
            if len(self.high_temperature) > 10:
                self.high_temperature.pop()

        if data.high_light:
            self.high_light.append(data.high_light)
            if len(self.high_light) > 10:
                self.high_light.pop()
        if data.picture_path:
            self.pictures.append(data.picture_path)

        if data.uptime:
            self.uptimes.update(data.uptime)
