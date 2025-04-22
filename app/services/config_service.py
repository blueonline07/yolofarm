import json

from app.patterns.observer import Subject
from app.patterns.singleton import Singleton
from app.repository.config_threshold import ThresholdRepository
from app.repository.user import UserRepository
from app.services.notification import ThresholdNotifier
from app.services.utils import ConfigThreshold



class ThresholdService(Singleton, Subject):
    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        self.repository = ThresholdRepository()
        self.attach(ThresholdNotifier())

    def get_all_thresholds(self):
        with self.repository.file_path.open('r') as f:
            data = json.load(f)
        return data

    def get_threshold(self, topic):
        return self.repository.get_threshold(topic)

    def set_threshold(self, topic, val, bound):
        self.notify(ConfigThreshold(topic, val, bound))
        return self.repository.set_threshold(topic, val ,bound)

class PermissionService(Singleton):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.__user_repository = UserRepository.get_instance()

    def update_permission(self, email, permissions):
        try:
            user = self.__user_repository.get_user_by_email(email)
            if not user:
                raise Exception("User not found")
            user['permissions'] = permissions
            self.__user_repository.update_by_email(email, user)
        except Exception as e:
            raise e

    def get_authorized_users(self, topic):
        try:
            users = self.__user_repository.get_all_users()
            authorized_users = [user['email'] for user in users if topic in user['permissions']]
            return authorized_users
        except Exception as e:
            raise e