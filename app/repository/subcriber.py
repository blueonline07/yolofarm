from pymongo import MongoClient
from app.config import MONGODB_URI
from app.patterns.singleton import Singleton

class SubscriberRepository(Singleton):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.subs = self.db['subcribers']

    def add(self, data):
        if self.subs.find_one(data):
            return data
        try:
            self.subs.insert_one(data)
        except Exception as e:
            raise e
        
        return data

    def get_all(self):
        try:
            return list(self.subs.find())
        except Exception as e:
            raise e

    def get_all_by_channel(self, channel):
        try:
            all = self.subs.find()
            result = [
                {
                    'email': sub['email'],
                    'channel': sub['channels']
                }
                for sub in all if channel in sub['channels']
            ]
            return result
        except Exception as e:
            raise e
        