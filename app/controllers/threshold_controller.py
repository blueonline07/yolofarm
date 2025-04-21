from flask import Blueprint, request
from app.decorators.auth import jwt_required
from app.services.config_service import ThresholdService

tv = ThresholdService()
threshold_bp = Blueprint('threshold', __name__)

@threshold_bp.route('', methods=['POST'])
@jwt_required(role=['admin'])
def config():
    data = request.json
    topic = data.get('topic')
    lower = data.get('lower')
    upper = data.get('upper')
    if topic and lower and upper:
        tv.set_threshold(topic, lower, upper)
        return f"threshold set for {topic} between {lower} and {upper}"
    else:
        return "invalid input", 400

@threshold_bp.route('', methods=['GET'])
@jwt_required(role=['admin', 'user'])
def get_config():
    return tv.get_all_thresholds(), 200