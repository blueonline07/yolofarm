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

    def get_logs(self):
        try:
            return list(str(self.logs.find()))
        except Exception as e:
            raise e