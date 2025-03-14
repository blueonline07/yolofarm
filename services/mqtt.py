from Adafruit_IO import MQTTClient
from config import ADAFRUIT_USERNAME, ADAFRUIT_KEY
from repositories.activities import ActivityRepository
from services.strategy import SimpleDecisionStrategy
from queue import Queue

event_queue = Queue()

class AdafruitService():
    def __init__(self):
        self.feeds = ['temp', 'humidity', 'moisture', 'light']
        self.client = MQTTClient(ADAFRUIT_USERNAME, ADAFRUIT_KEY)
        self.client.on_message = self.message_received
        self.client.connect()

        for feed in self.feeds:
            self.client.subscribe(feed)

        self.client.loop_background()
        self.strategy = SimpleDecisionStrategy()
        self.activity_repo = ActivityRepository()

    def publish_val(self, topic, val, activity_type = 'AUTO'):
        self.activity_repo.create(val, activity_type, topic)
        self.client.publish(topic, str(val))

    def message_received(self, client, topic, message):
        # feed , msg = self.strategy.make_decision(topic, message)
        # self.publish_val(feed, msg)
        print(f'Received value {message} from topic {topic}')
        event_queue.put((topic, float(message)))


