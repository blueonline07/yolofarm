from abc import ABC, abstractmethod
from config import ADAFRUIT_USERNAME, ADAFRUIT_KEY
from Adafruit_IO import MQTTClient
from patterns.observer import Subject
import requests


# Strategy Pattern for data retrieval methods
class DataRetrievalStrategy(ABC):
    @abstractmethod
    def get_client(self):
        pass


class RestApiStrategy(DataRetrievalStrategy):
    def __init__(self):
        self.client = RestClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)

    def get_client(self):
        return self.client



class MqttStrategy(DataRetrievalStrategy, Subject):
    def __init__(self, feed_key):
        super().__init__()
        self.client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
        self.client.on_message = self.message
        self.client.connect()
        self.client.subscribe(feed_key)
        self.client.loop_background()

    def message(self, client, feed_id, payload):
        self.notify(payload)

    def attach(self, observer):
        self._observers.append(observer)
        return self

    def get_client(self):
        return self.client

class RestClient:
    def __init__(self, username, key):
        self.username = username
        self.key = key

    def get_data(self, feed_key):
        resp = requests.get(f"https://io.adafruit.com/api/v2/{self.username}/feeds/{feed_key}/data", headers={"X-AIO-Key": self.key}).json()
        return [{"created_at": item["created_at"], "value": item["value"]} for item in resp]

