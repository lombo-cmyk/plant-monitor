from typing import Any, Callable

from paho.mqtt.client import Client
from pydantic import BaseModel


class MqttClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handlers = dict()
        self.on_message = self.on_message_custom

    def publish(self, topic: str, payload: BaseModel):
        super().publish(topic=topic, payload=payload.model_dump_json())

    def on_message_custom(self, client, userdata, msg):
        handler, payload_class = self.handlers[msg.topic]
        handler(
            self, msg.topic, payload_class.model_validate_json(msg.payload.decode())
        )

    def subscribe(
        self,
        topic: str,
        handler: Callable[[str, BaseModel], Any],
        payload_class: BaseModel,
    ):
        self.handlers[topic] = handler, payload_class
        super().subscribe(topic)
