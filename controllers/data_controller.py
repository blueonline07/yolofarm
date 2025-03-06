from flask import Blueprint, jsonify
from services.adafruit_service import AdafruitService
data_bp = Blueprint('data', __name__)
service = AdafruitService()
@data_bp.route('/data/<feed_key>')
def get_feed_data(feed_key):
    data = service.get_data(feed_key)
    return jsonify(data)
