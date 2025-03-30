from logging import Logger
from typing import Any, Callable

from paho.mqtt.client import Client
from pydantic import BaseModel


class MqttClient(Client):

    def __init__(self, logger: Logger, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.custom_logger = logger
        self.handlers = dict()
        self.on_message = self.on_message_custom

    def publish(self, topic: str, payload: BaseModel) -> None:
        super().publish(topic=topic, payload=payload.model_dump_json())

    def on_message_custom(self, client, userdata, msg) -> None:
        handler, payload_class = self.handlers[msg.topic]
        try:
            handler(
                self, msg.topic, payload_class.model_validate_json(msg.payload.decode())
            )
        except Exception:
            self.custom_logger.exception(f"Couldn't execute handler on {msg.topic}")

    def subscribe(
        self,
        topic: str,
        handler: Callable[[str, BaseModel], Any],
        payload_class: BaseModel,
    ) -> None:
        self.handlers[topic] = handler, payload_class
        super().subscribe(topic)
