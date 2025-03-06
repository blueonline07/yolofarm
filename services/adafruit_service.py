from patterns.strategy import RestApiStrategy, MqttStrategy
from patterns.observer import Observer
from repositories.notifications import NotificationRepository
import logging

logger = logging.getLogger(__name__)

class AdafruitService(Observer):
    def __init__(self):
        super().__init__()
        self.feeds = {
            'light': RestApiStrategy('light').get_client(),
            'temp': MqttStrategy('temp').attach(self).get_client(),
        }
        self.notifications_repo = NotificationRepository()

    def get_data(self, feed_key):
        try:
            return self.feeds[feed_key].get_data()
        except AttributeError:
            logger.error(f"Feed {feed_key} is using MQTT, please use the update method instead")
            return "Feed is using MQTT, please use the update method instead"

    def update(self, data):
        #TODO: do the checking here, then notify to user
        self.notifications_repo.create_notification(data)