from flask import Flask
from services.mqtt import AdafruitService
from flask import request
from flask_cors import CORS
import logging
from flask_socketio import SocketIO

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

sv = AdafruitService(socketio)

@app.route('/<feed>', methods=['POST'])
def post_data(feed):
    val = request.json.get('value')
    sv.publish_val(feed, val)
    return f"value {val} added to feed {feed}"

if __name__ == '__main__':
    socketio.run(app, debug=True)