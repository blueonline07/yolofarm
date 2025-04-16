from enum import Enum
from abc import ABC
from datetime import datetime
from app.patterns.observer import Observer
import json

class Bound(Enum):
    HIGHER = "higher"
    LOWER = "lower"

class Action(Enum):
    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"


class Notification(ABC):
    _timestamp: datetime
    pass

class Alert:
    def __init__(self, topic: str, issue: Bound, value: float):
        self.topic = topic
        self.issue = issue
        self.value = value
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"Alert(topic={self.topic}, issue={self.issue}, value={self.value}, timestamp={self.timestamp})"

class Action:
    def __init__(self, action: Action, device: str):
        self.action = action
        self.device = device
        self.timestamp = datetime.now()
    
    def __repr__(self):
        return f"Log(action={self.action}, device={self.device}, timestamp={self.timestamp})"
        


class Visitor:
    def visit(self, topic, value):
        if topic == 'temp':
            return self.visit_temp(value)
        elif topic == 'humidity':
            return self.visit_humidity(value)
        elif topic == 'moisture':
            return self.visit_moisture(value)
        elif topic == 'light':
            return self.visit_light(value)
        
    def visit_temp(self, value):
        if value > 32:
            return Alert(topic='temp', issue=Bound.HIGHER, value=value)
        elif value < 18:
            return Alert(topic='temp', issue=Bound.LOWER, value=value)
        return None
    def visit_humidity(self, value):
        if value > 80:
            return Alert(topic='humidity', issue=Bound.HIGHER, value=value)
        elif value < 40:
            return Alert(topic='humidity', issue=Bound.LOWER, value=value)
        return None
    def visit_moisture(self, value):
        if value > 70:
            return Alert(topic='moisture', issue=Bound.HIGHER, value=value)
        elif value < 30:
            return Alert(topic='moisture', issue=Bound.LOWER, value=value)
        return None
    def visit_light(self, value):
        if value > 1000:
            return Alert(topic='light', issue=Bound.HIGHER, value=value)
        elif value < 200:
            return Alert(topic='light', issue=Bound.LOWER, value=value)
        return None

def make_decision(topic: str, value: float) -> Alert:
    v = Visitor()
    return v.visit(topic, float(value))
