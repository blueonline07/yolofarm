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
        user_data = {
            'email': email,
        }
        try:
            self.subs.insert_one(user_data)
        except Exception as e:
            raise e
        
        return user_data
    
    def get_all(self):
        try:
            return list(self.subs.find())
        except Exception as e:
            raise e