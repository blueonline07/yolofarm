import json
from pathlib import Path

from app.patterns.singleton import Singleton


class ThresholdRepository(Singleton):
    def __init__(self, file_path='thresholds.json'):

        if self._initialized:
            return
        self._initialized = True
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps({}))

    def get_threshold(self, topic):
        with self.file_path.open('r') as f:
            data = json.load(f)
        return data.get(topic, {})

    def set_threshold(self, topic, lower, upper):
        with self.file_path.open('r') as f:
            data = json.load(f)
        data[topic] = {'lower': lower, 'upper': upper}
        with self.file_path.open('w') as f:
            json.dump(data, f, indent=4)

class ThresholdService(Singleton):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.repository = ThresholdRepository()

    def get_threshold(self, topic):
        return self.repository.get_threshold(topic)

    def set_threshold(self, topic, lower, upper):
        return self.repository.set_threshold(topic, lower, upper)