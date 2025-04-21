from pymongo import MongoClient
from app.config import MONGODB_URI
from app.patterns.singleton import Singleton
from app.repository.user import UserRepository

class SubscriberRepository(Singleton):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.user_repository = UserRepository.get_instance()

    def add(self, data):
        user = self.user_repository.get_user_by_email(data['email'])
        if not user:
            raise Exception("User not found")
        try:
            print(user)
            user['channels'] = list(set(user['channels']).union(data['channels']))
            self.user_repository.update_by_email(user['email'], user)
        except Exception as e:
            raise e

    def remove(self, data):
        user = self.user_repository.get_user_by_email(data['email'])
        if not user:
            raise Exception("User not found")
        try:
            user['channels'] = list(set(user['channels']).difference(data['channels']))
            print(user)
            self.user_repository.update_by_email(user['email'], user)
        except Exception as e:
            raise e

    def get_all_by_channel(self, channel):
        try:
            return list(self.user_repository.get_users_by_channel(channel))
        except Exception as e:
            raise e
        