from enum import Enum
from abc import ABC
from datetime import datetime
from app.services.config_service import ThresholdService

class Bound(Enum):
    HIGHER = "higher"
    LOWER = "lower"

class Action(Enum):
    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"

class Notification(ABC):
    _topic: str
    _value: float
    _timestamp: datetime
    pass

class Alert:
    def __init__(self, topic: str, issue: Bound, value: float):
        self._topic = topic
        self.issue = issue
        self._value = value
        self._timestamp = datetime.now()

    def __repr__(self):
        return f"Alert(topic={self._topic}, issue={self.issue}, value={self._value}, timestamp={self._timestamp})"

class Control:
    def __init__(self, topic: str, value: float):
        if value == 1:
            value = Action.TURN_ON
        elif value == 0:
            value = Action.TURN_OFF
        self._value = value
        self._topic = topic
        self._timestamp = datetime.now()
    
    def __repr__(self):
        return f"Log(action={self._value}, device={self._topic}, timestamp={self._timestamp})"
        

class Decision:
    o = ThresholdService()
    @classmethod
    def simple(cls, topic, value):
        if topic not in ['temp', 'humidity', 'moisture', 'light']:
            raise NotImplementedError
        if value > cls.o.get_threshold(topic)['upper']:
            return Alert(topic, Bound.HIGHER, value)
        elif value < cls.o.get_threshold(topic)['lower']:
            return Alert(topic, Bound.LOWER, value)

