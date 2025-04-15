from Adafruit_IO import MQTTClient
from flask import current_app as app
from services.utils import make_decision
from config import ADAFRUIT_KEY, ADAFRUIT_USERNAME
from patterns.observer import Subject
import json

feeds = ['temp', 'humidity', 'moisture', 'light']

class AdafruitService(Subject):

    def __init__(self):

        self.client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
        self.client.on_message = self.message_received
        self.client.connect()
        for feed in feeds:
            self.client.subscribe(feed)

        self.client.loop_background()

    def publish_val(self, topic, val):
        self.client.publish(topic, str(val))

    def message_received(self, client, topic, message):
        print(f"Received message '{message}' on topic '{topic}'")
        app.emit('message', json.dumps({'topic': topic, 'value': message}))

        self.notify(make_decision(topic, message))

