from patterns.singleton import Singleton
from patterns.strategy import RestApiStrategy, MqttStrategy
from patterns.observer import Observer
from repositories.notifications import NotificationRepository
import logging

logger = logging.getLogger(__name__)

class AdafruitService(Observer, Singleton):
    def __init__(self):
        super().__init__()
        self.feeds = {
            'light': MqttStrategy('light').attach(self).get_client(),
            'temp': MqttStrategy('temp').attach(self).get_client(),
        }
        self.rest_client = RestApiStrategy().get_client()
        self.notifications_repo = NotificationRepository()

    def get_data(self, feed_keys):
        try:
            return {feed_key: self.rest_client.get_data(feed_key) for feed_key in feed_keys}
        except Exception as e:
            logger.error(e)
            return "Error while fetching data from Adafruit"

    def update(self, data):
        #TODO: do the checking here, then notify to user
        self.notifications_repo.create_notification(data)
