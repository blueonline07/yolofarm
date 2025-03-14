from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_URI
from patterns.singleton import Singleton

class ActivityRepository(Singleton):
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_database('yolofarm')
        self.collection = self.db.activities


    def create(self, action, type,  device):
        """
        save an activity
        :param device:
        :param type:
        :param action:
        :return: id of the activity
        """
        activity = {
            'action': action,
            'type': type,
            'device': device,
            'created_at': datetime.now()
        }
        res = self.collection.insert_one(activity)
        return str(res.inserted_id)

    def get_all(self):
        """
        Get all notifications
        :return: list of notifications
        """
        return list(self.collection.find())
