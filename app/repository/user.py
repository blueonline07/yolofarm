from pymongo import MongoClient
from app.config import MONGODB_URI
import bcrypt
from app.patterns.singleton import Singleton

class UserRepository(Singleton):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.users = self.db['users']


    def create_user(self, user):
        email = user.get('email')
        password = user.get('password')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'email': email,
            'password': hashed_password,
            'role':'user'
        }
        try:
            existing_user = self.get_user_by_email(email)
            if existing_user:
                raise Exception("User already exists")
            self.users.insert_one(user_data)
        except Exception as e:
            raise e
        
        return user

    def get_user_by_email(self, email):
        try:
            return self.users.find_one({'email': email})

        except Exception as e:
            raise e

    def get_user_by_id(self, user_id):
        try:
            return self.users.find_one({'_id': user_id})

        except Exception as e:
            raise e

    def get_all_users(self):
        try:
            return list(self.users.find())

        except Exception as e:
            raise e

    def delete_user(self, user_id):
        try:
            self.users.delete_one({'_id': user_id})

        except Exception as e:
            raise e