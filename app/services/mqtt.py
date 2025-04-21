from Adafruit_IO import MQTTClient
from app.config import ADAFRUIT_KEY, ADAFRUIT_USERNAME
from app.patterns.observer import Subject
from app.patterns.singleton import Singleton
from app.services.utils import Action, Log

feeds = ['temp', 'humidity', 'moisture', 'light']

class AdafruitService(Singleton, Subject):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        super().__init__()
        self.client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
        self.client.on_message = self.message_received
        self.client.connect()
        for feed in feeds:
            self.client.subscribe(feed)

        self.client.loop_background()


    def publish_val(self,user, topic, val):
        if topic in feeds:
            raise Exception("Invalid topic")
        print(f"Publishing value '{val}' to topic '{topic}'")
        self.client.publish(topic, val)
        self.notify(Action(user, topic, float(val)))

    def message_received(self, client, topic, message):
        print(f"Received message '{message}' on topic '{topic}'")
        self.notify(Log(topic, float(message)))

