from services.mqtt import AdafruitService
from flask import Blueprint, request

sv = AdafruitService()
data_bp = Blueprint('data', __name__)

@data_bp.route('/<feed>', methods=['POST'])
def post_data(feed):
    val = request.json.get('value')
    sv.publish_val(feed, val)
    return f"value {val} added to feed {feed}"


