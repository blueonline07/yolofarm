import pymongo
from pymongo import MongoClient
from app.config import MONGODB_URI
from app.patterns.singleton import Singleton


class LoggingService(Singleton):
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.logs = self.db['logs']

    def log(self, data):
        try:
            self.logs.insert_one(data)
        except Exception as e:
            raise e

    def get_logs(self, lim):
        try:
            return list(self.logs.find().limit(lim).sort('timestamp', pymongo.DESCENDING))
        except Exception as e:
            raise e