from flask import Flask
from controllers.data_controller import data_bp

from flask_cors import CORS
from flask_socketio import SocketIO


app = Flask(__name__)


CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(data_bp, url_prefix='/data')

if __name__ == '__main__':
    socketio.run(app)