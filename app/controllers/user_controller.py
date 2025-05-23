from bson import ObjectId
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
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = user_repository.get_user_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            payload = {
                'email': email,
                'role': user['role'],
                'exp': datetime.datetime.now() + datetime.timedelta(minutes=30)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            return jsonify({"token":token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required(role=['admin'])
def get_user_by_id(user_id):
    try:
        user_id = ObjectId(user_id)
        user = user_repository.get_user_by_id(user_id)
        if user:
            return jsonify({
                "_id": str(user['_id']),
                "email": user['email'],
                "role": user['role'],
                "channels": user['channels'],
                "permissions": user['permissions']
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/', methods=['GET'])
@jwt_required(role=['admin'])
def get_all_users():
    try:
        lim = request.args.get('limit', default=10, type=int)
        users = [{"_id": str(user['_id']), "email": user['email'], "role": user['role'], "channels": user['channels'], "permissions": user['permissions']} for user in user_repository.get_all_users(lim)]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required(role=['admin'])
def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
        result = user_repository.delete_user(user_id)
        if result:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/me', methods=['GET'])
@jwt_required(role=['admin', 'user'])
def get_current_user():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        email = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])['email']
        user = user_repository.get_user_by_email(email)
        if user:
            return jsonify({
                "_id": str(user['_id']),
                "email": user['email'],
                "role": user['role'],
                "channels": user['channels'],
                "permissions": user['permissions']
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
