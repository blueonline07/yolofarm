from app.patterns.observer import Observer
from app.patterns.singleton import Singleton
import json

class SocketObserver(Singleton, Observer):
    def __init__(self, socket):
        if self._initialized:
            return
        self._initialized = True
        self.socket = socket

    def update(self, data):
        topic = data['topic']
        message = data['value']
        self.socket.emit('message', json.dumps({'topic': topic, 'value': message}))