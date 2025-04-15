from flask import Flask, request
from services.mqtt import AdafruitService

from flask_cors import CORS
from flask_socketio import SocketIO


app = Flask(__name__)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

sv = AdafruitService(socket=socketio)

@app.route('/<feed>', methods=['POST'])
def post_data(feed):
    val = request.json.get('value')
    sv.publish_val(feed, val)
    return f"value {val} added to feed {feed}"

if __name__ == '__main__':
    socketio.run(app)