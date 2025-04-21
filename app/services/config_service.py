import json
from pathlib import Path

from app.patterns.singleton import Singleton
from app.repository.user import UserRepository


class ThresholdRepository(Singleton):
    def __init__(self, file_path='thresholds.json'):

        if self._initialized:
            return
        self._initialized = True
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps({}))

    def get_threshold(self, topic):
        with self.file_path.open('r') as f:
            data = json.load(f)
        return data.get(topic, {})

    def set_threshold(self, topic, lower, upper):
        with self.file_path.open('r') as f:
            data = json.load(f)
        data[topic] = {'lower': lower, 'upper': upper}
        with self.file_path.open('w') as f:
            json.dump(data, f, indent=4)

class ThresholdService(Singleton):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.repository = ThresholdRepository()

    def get_all_thresholds(self):
        with self.repository.file_path.open('r') as f:
            data = json.load(f)
        return data

    def get_threshold(self, topic):
        return self.repository.get_threshold(topic)

    def set_threshold(self, topic, lower, upper):
        # self.notify()
        return self.repository.set_threshold(topic, lower, upper)


class PermissionService(Singleton):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.__user_repository = UserRepository.get_instance()

    def add_permission(self, email, permissions):
        try:
            user = self.__user_repository.get_user_by_email(email)
            if not user:
                raise Exception("User not found")
            user['permissions'] = list(set(user['permissions']).union(permissions))
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