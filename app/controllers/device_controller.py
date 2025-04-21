import threading

import jwt

from app import JWT_SECRET
from app.repository import user
from app.services.mqtt import AdafruitService
from flask.blueprints import Blueprint
from flask import request
from app.decorators.auth import jwt_required
from app.services.config_service import PermissionService

sv = AdafruitService()
pv = PermissionService()
device_bp = Blueprint('device', __name__)
feed_locks = {}

@device_bp.route('/<feed>', methods=['POST'])
@jwt_required(role=['admin', 'user'])
def post_data(feed):
    val = request.json.get('value')
    role = request.json.get('role')

    tok = request.headers.get('Authorization').split(' ')[1]
    user_email = jwt.decode(tok, JWT_SECRET, algorithms=['HS256'])['email']

    if feed not in feed_locks:
        feed_locks[feed] = threading.Lock()

    lock = feed_locks[feed]
    with lock:
        if user_email in pv.get_authorized_users(feed) or role == 'admin':
        #TODO: restrict topic to fan, pump, led only
            sv.publish_val(feed, val)
            return f"value {val} added to feed {feed}"

        return "Unauthorized user", 403



@device_bp.route('/permission', methods=['POST'])
@jwt_required(role=['admin'])
def add_permission():
    data = request.json
    email = data.get('email')
    topics = data.get('topics')
    try:
        pv.add_permission(email, topics)
        return "permission added successfully", 200
    except Exception as e:
        return str(e), 500
