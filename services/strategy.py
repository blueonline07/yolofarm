from abc import ABC, abstractmethod

from patterns.singleton import Singleton
from repositories.notifications import NotificationRepository


class DecisionStrategy(ABC):
    @abstractmethod
    def make_decision(self,topic, data):
        pass

    @abstractmethod
    def send_notification(self, topic, data):
        pass

class SimpleDecisionStrategy(DecisionStrategy, Singleton):
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def make_decision(self, topic, data):
        if topic == 'temp' and float(data) > 32:
            return 'fan', 1
        elif topic == 'temp' and float(data) < 18:
            return 'fan', 0
        elif topic == 'moisture' and float(data) < 50:
            return 'pump', 1
        elif topic == 'light' and float(data) < 50:
            return 'bulb', 1

    def send_notification(self, topic, data):
        self.notification_repo.create('haha', 'INFO')
        #TODO: implement a websocket to send notification real time
