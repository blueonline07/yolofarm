from abc import ABC, abstractmethod

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, data):
        if data is not None:
            list(map(lambda observer: observer.update(data), self._observers))

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass