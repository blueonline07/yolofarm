from flask import Flask, request
from app.services.mqtt import AdafruitService
from app.controllers.user_controller import user_bp
from flask_cors import CORS
from flask_socketio import SocketIO
from app.services.notification import EmailNotification
from app.services.socket_service import SocketObserver
from app.decorators.auth import jwt_required


def create_app():
    app = Flask(__name__)

    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    sv = AdafruitService()
    sv.attach(SocketObserver(socketio))
    sv.attach(EmailNotification())

    app.register_blueprint(user_bp, url_prefix='/users')

    @app.route('/<feed>', methods=['POST'])
    @jwt_required(role=['admin'])
    def post_data(feed):
        val = request.json.get('value')
        sv.publish_val(feed, val)
        return f"value {val} added to feed {feed}"

    
    @app.route('/subcription', methods=['POST'])
    @jwt_required(role=['user', 'admin'])
    def subscribe():
        data = request.json
        email = data.get('email')
        EmailNotification().add_subcriber(email)
        return "subscribed successfully", 200

    return socketio, app