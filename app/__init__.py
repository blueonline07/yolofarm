from flask import Flask, request

from app.config import JWT_SECRET
from app.services.mqtt import AdafruitService
from app.controllers.threshold_controller import threshold_bp
from app.controllers.user_controller import user_bp
from app.controllers.device_controller import device_bp
from flask_cors import CORS
from flask_socketio import SocketIO
from app.services.notification import BoundaryNotifier, BaseNotifier, ActionNotifier
from app.services.socket_service import SocketObserver
from app.decorators.auth import jwt_required
from app.services.config_service import ThresholdService
from app.controllers.log_controller import log_bp
import jwt

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    sv = AdafruitService()
    sv.attach(SocketObserver(socketio))
    sv.attach(BoundaryNotifier())
    sv.attach(ActionNotifier())
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(device_bp, url_prefix='/devices')
    app.register_blueprint(threshold_bp, url_prefix='/config')
    app.register_blueprint(log_bp, url_prefix='/logs')

    
    @app.route('/subscription', methods=['POST'])
    @jwt_required(role=['user', 'admin'])
    def subscribe():
        data = request.json
        channels = data.get('channels')
        tok = request.headers.get('Authorization')
        tok = tok.split(" ")[1]
        decoded = jwt.decode(tok, JWT_SECRET, algorithms=['HS256'])
        email = decoded.get('email')
        BaseNotifier().update_subscriber({"email": email, "channels": channels})
        return "subscribed successfully", 200


    return socketio, app