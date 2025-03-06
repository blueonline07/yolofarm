from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_URI
from patterns.singleton import Singleton


class NotificationRepository(Singleton):
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database('yolofarm')
        self.collection = self.db.notifications


    def create_notification(self, message):
        """
        Create a notification for a user
        :param message:
        :return:
        """
        notification = {
            'message': message,
            'created_at': datetime.now()
        }
        res = self.collection.insert_one(notification)
        print(res.inserted_id)
        return str(res.inserted_id)
