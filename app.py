from flask import Flask
from controllers.data_controller import data_bp
from services.mqtt import AdafruitService
from flask_cors import CORS
from flask_socketio import SocketIO


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
AdafruitService(socket=socketio)
app.register_blueprint(data_bp, url_prefix='/data')

@app.route('/')
def index():
    return 'Yolo farm đang chạy trên Azure 🚀'

if __name__ == '__main__':
    socketio.run(app)