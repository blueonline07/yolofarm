from pymongo import MongoClient
from app.config import MONGODB_URI
import bcrypt

class UserRepository:

    def __init__(self):
        # Use environment variable or default to localhost if not provided
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['yolofarm']
        self.users = self.db['users']
        print(list(self.users.find()))
        
    def close_connection(self):
        # Close the MongoDB connection when done
        if hasattr(self, 'client'):
            self.client.close()
    
    def create_user(self, user):
        email = user.get('email')
        password = user.get('password')
        phone = user.get('phone')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'email': email,
            'password': hashed_password,
            'phone': phone
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
    