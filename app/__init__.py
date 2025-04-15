from flask import Flask, request
from app.services.mqtt import AdafruitService
from app.controllers.user_controller import user_bp
from flask_cors import CORS
from flask_socketio import SocketIO
from app.services.notification import EmailNotification


def create_app():
    app = Flask(__name__)

    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    sv = AdafruitService(socket=socketio)
    app.register_blueprint(user_bp, url_prefix='/users')

    @app.route('/<feed>', methods=['POST'])
    def post_data(feed):
        val = request.json.get('value')
        sv.publish_val(feed, val)
        return f"value {val} added to feed {feed}"

    @app.route('/subcription', methods=['POST'])
    def subscribe():
        data = request.json
        email = data.get('email')
        if not email:
            return "Email is required", 400
        if email in sv._observers:
            return f"{email} is already subscribed", 400
        sv.attach(EmailNotification(email))
        return f"Subscribed {email} for notifications", 200
    return socketio, app