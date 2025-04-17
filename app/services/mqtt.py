from Adafruit_IO import MQTTClient
from app.services.utils import make_decision
from app.config import ADAFRUIT_KEY, ADAFRUIT_USERNAME
from app.patterns.observer import Subject
from app.patterns.singleton import Singleton

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


    def publish_val(self, topic, val):
        self.client.publish(topic, str(val))
        self.notify({
            'topic': topic,
            'value': val
        })

    def message_received(self, client, topic, message):
        print(f"Received message '{message}' on topic '{topic}'")
        data = {
            'topic': topic,
            'value': message
        }
        self.notify(data)

