from flask import Blueprint, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == 'admin' and password == 'admin':
        return {'message': 'User authenticated successfully'}, 200
    
    return {'message': 'Invalid credentials'}, 401