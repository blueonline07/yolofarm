from datetime import datetime

class Log:
    def __init__(self, topic: str, value: float):
        self._topic = topic
        self._value = value
        self._timestamp = datetime.now()

class Alert(Log):
    def __init__(self, topic: str, value: float):
        super().__init__(topic, value)

    def __repr__(self):
        return f"Alert(topic={self._topic}, value={self._value}, timestamp={self._timestamp})"

class Action(Log):
    def __init__(self,user:str, topic: str, value: float):
        self.user = user
        super().__init__(topic, value)
    
    def __repr__(self):
        return f"Action(user={self.user}, action={self._value}, device={self._topic}, timestamp={self._timestamp})"

class ConfigThreshold(Log):
    def __init__(self, topic: str, val: float, bound: str):
        super().__init__(topic, val)
        self.bound = bound
    def __repr__(self):
        return f"ConfigThreshold(topic={self._topic}, threshold={self._value}, bound={self.bound}, timestamp={self._timestamp})"
