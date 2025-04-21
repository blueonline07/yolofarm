from flask import Blueprint, request, jsonify

from app.decorators.auth import jwt_required
from app.services.logging_service import LoggingService


log_bp = Blueprint('logs', __name__)


@log_bp.route('/', methods=['GET'])
@jwt_required(['admin'])
def get_logs():
    """
    Get all logs
    """
    lim = request.args.get('limit', default=10, type=int)
    logs = LoggingService().get_logs(lim)
    return jsonify([
        {
            'content': log['content'],
            'timestamp': log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        }
        for log in logs
    ]), 200
