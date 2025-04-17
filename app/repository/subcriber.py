from pymongo import MongoClient
from app.config import MONGODB_URI
from app.patterns.singleton import Singleton



class SubcriberRepository(Singleton):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.subs = self.db['subcribers']

    def add(self, email):
        data = {
            'email': email
        }
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
        