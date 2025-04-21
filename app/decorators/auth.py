import jwt
from functools import wraps
from flask import request
from app.config import JWT_SECRET


def jwt_required(role=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            if not token:
                return {'error': 'Token is missing!'}, 401
            try:
                tok = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                if tok['role'] not in role:
                    return {'error': 'You do not have permission to access this resource!'}, 403

            except jwt.ExpiredSignatureError:
                return {'error': 'Token has expired!'}, 401
            except jwt.InvalidTokenError:
                return {'error': 'Invalid token!'}, 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator