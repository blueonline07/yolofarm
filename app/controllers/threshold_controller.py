from flask import Blueprint, request
from app.decorators.auth import jwt_required
from app.services.config_service import ThresholdService

tv = ThresholdService()
threshold_bp = Blueprint('threshold', __name__)

@threshold_bp.route('/', methods=['POST'])
@jwt_required(role=['admin'])
def config():
    data = request.json
    topic = data.get('topic')
    val = data.get('value')
    bound = data.get('bound')
    try:
        tv.set_threshold(topic, val, bound)
        return f"threshold set {val} for {topic} at {bound}", 200
    except Exception as e:
        return str(e), 500

@threshold_bp.route('', methods=['GET'])
@jwt_required(role=['admin', 'user'])
def get_config():
    return tv.get_all_thresholds(), 200