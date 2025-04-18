from flask import Flask, request

from app.config import JWT_SECRET
from app.services.mqtt import AdafruitService
from app.controllers.user_controller import user_bp
from flask_cors import CORS
from flask_socketio import SocketIO
from app.services.notification import BoundaryNotifier, BaseNotifier, ActionNotifier
from app.services.socket_service import SocketObserver
from app.decorators.auth import jwt_required
from app.services.config_service import ThresholdService
import jwt

def create_app():
    app = Flask(__name__)
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    sv = AdafruitService()
    sv.attach(SocketObserver(socketio))
    sv.attach(BoundaryNotifier())
    sv.attach(ActionNotifier())
    tv = ThresholdService()
    app.register_blueprint(user_bp, url_prefix='/users')

    @app.route('/<feed>', methods=['POST'])
    @jwt_required(role=['admin'])
    def post_data(feed):
        val = request.json.get('value')
        #TODO: restrict topic to fan, pump, led only
        sv.publish_val(feed, val)
        return f"value {val} added to feed {feed}"

    
    @app.route('/subcription', methods=['POST'])
    @jwt_required(role=['user', 'admin'])
    def subscribe():
        data = request.json
        channels = data.get('channels')
        tok = request.headers.get('Authorization')
        tok = tok.split(" ")[1]
        decoded = jwt.decode(tok, JWT_SECRET, algorithms=['HS256'])
        email = decoded.get('email')
        BaseNotifier().add_subcriber({"email": email, "channels": channels})
        return "subscribed successfully", 200

    @app.route('/config', methods=['POST'])
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

    return socketio, app