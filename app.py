from flask import Flask
from services.mqtt import AdafruitService
from flask import request, Response
from flask_cors import CORS
import logging
import json
from services.mqtt import event_queue


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = Flask(__name__)
CORS(app)

sv = AdafruitService()
@app.route("/stream")
def stream():
    def event_stream():
        while True:
            data = event_queue.get()  # Block until new data arrives
            yield f"data: {json.dumps({'type':data[0], 'value':data[1]})}\n\n"
            print(data)

    return Response(event_stream(), mimetype="text/event-stream")
@app.route('/')
def hello_world():
    return 'IoT Backend API'

@app.route('/<feed>', methods=['POST'])
def post_data(feed):
    val = request.json.get('value')
    sv.publish_val(feed, val)
    return f"value {val} added to feed {feed}"

if __name__ == '__main__':
    app.run(debug=True)