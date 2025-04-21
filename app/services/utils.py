from datetime import datetime
from app.services.config_service import ThresholdService

class Notification:
    def __init__(self, topic: str, value: float):
        self._topic = topic
        self._value = value
        self._timestamp = datetime.now()

class Alert(Notification):
    def __init__(self, topic: str, value: float):
        super().__init__(topic, value)

    def __repr__(self):
        return f"Alert(topic={self._topic}, value={self._value}, timestamp={self._timestamp})"

class Action(Notification):
    def __init__(self,user:str, topic: str, value: float):
        self.user = user
        super().__init__(topic, value)
    
    def __repr__(self):
        return f"Log(user={self.user}, action={self._value}, device={self._topic}, timestamp={self._timestamp})"

