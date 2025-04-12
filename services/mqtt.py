from Adafruit_IO import MQTTClient
from config import ADAFRUIT_USERNAME, ADAFRUIT_KEY
import json


feeds = ['temp', 'humidity', 'moisture', 'light']

class AdafruitService():
    _instance = None
    _initialized = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AdafruitService, cls).__new__(cls)
        return cls._instance

    def __init__(self, socketio):
        if not self._initialized:
            self.client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
            self.client.on_message = self.message_received
            self.client.connect()
            self.socket = socketio
            for feed in feeds:
                self.client.subscribe(feed)

            self.client.loop_background()
            self._initialized = True

    def publish_val(self, topic, val):
        self.client.publish(topic, str(val))

    def message_received(self, client, topic, message):
        print(f'Received value {message} from topic {topic}')
        self.socket.emit('message', json.dumps({'topic': topic, 'value': message}))

