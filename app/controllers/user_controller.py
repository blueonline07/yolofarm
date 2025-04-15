from flask import Blueprint, request, jsonify
from app.repository.user import UserRepository
from app.decorators.auth import jwt_required
import jwt
import bcrypt
from app.config import JWT_SECRET
from datetime import datetime

user_bp = Blueprint('user', __name__)
user_repository = UserRepository()

@user_bp.route('/', methods=['POST'])
def register():
    data = request.get_json()
    
    # Create new user
    try:
        user_repository.create_user(data)
        return jsonify({"message": "User created successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = user_repository.get_user_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            payload = {
                'email': user['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            return jsonify({"token":token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<email>', methods=['GET'])
@jwt_required
def get_user(email):
    try:
        user = user_repository.get_user_by_email(email)
        if user:
            return jsonify({"email": user['email']}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

