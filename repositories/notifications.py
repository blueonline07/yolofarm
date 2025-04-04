from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_URI
from patterns.singleton import Singleton
from enum import Enum

class NotificationType(Enum):
    INFO = 1
    WARNING = 2


class NotificationRepository(Singleton):
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database('yolofarm')
        self.collection = self.db.notifications


    def create(self, message, type):
        """
        Create a notification for a user
        :param type:
        :param message:
        :return: id of the notification
        """
        notification = {
            'message': message,
            'type': type,
            'created_at': datetime.now()
        }
        res = self.collection.insert_one(notification)
        return str(res.inserted_id)

    def get_all(self):
        """
        Get all notifications
        :return: list of notifications
        """
        return list(self.collection.find())
