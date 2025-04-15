from flask import Blueprint, request, jsonify
from app.repository.user import UserRepository
from app.decorators.auth import jwt_required
import jwt
import bcrypt
from app.config import JWT_SECRET
import datetime

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
    username = data.get('username')
    password = data.get('password')
    
    try:
        user = user_repository.get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            payload = {
                'username': username,
                'role': user['role'],
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            return jsonify({"token":token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<username>', methods=['GET'])
@jwt_required(role=['admin'])
def get_user(username):
    try:
        user = user_repository.get_user_by_username(username)
        if user:
            return jsonify({
                "username": user['username'],
                "email": user['email'],
                "phone": user['phone'],
                "role": user['role']
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

