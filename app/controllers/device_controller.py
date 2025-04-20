from app.services.mqtt import AdafruitService
from flask.blueprints import Blueprint
from flask import request
from app.decorators.auth import jwt_required
from app.services.config_service import PermissionService

sv = AdafruitService()
pv = PermissionService()
device_bp = Blueprint('device', __name__)

@device_bp.route('/<feed>', methods=['POST'])
@jwt_required(role=['admin', 'user'])
def post_data(feed):
    val = request.json.get('value')
    #TODO: restrict topic to fan, pump, led only
    sv.publish_val(feed, val)
    return f"value {val} added to feed {feed}"


# @device_bp.route('/permission', methods=['POST'])
# @jwt_required(role=['admin'])
# def add_permission():
#     data = request.json
#     user = data.get('id_')
#     topics = data.get('topics')
#     try:
#         pv.add_permission(user, topics)
#         return "permission added successfully", 200
#     except Exception as e:
#         return str(e), 500
