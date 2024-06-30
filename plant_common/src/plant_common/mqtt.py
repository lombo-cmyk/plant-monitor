from paho.mqtt.client import Client
from pydantic import BaseModel


class MqttClient(Client):

    def publish(self, topic: str, payload: BaseModel):
        super().publish(topic=topic, payload=payload.model_dump_json())
