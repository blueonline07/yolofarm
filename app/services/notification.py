from pymongo import MongoClient

from app.patterns.observer import Observer
import smtplib
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.repository.subscriber import SubscriberRepository
from app.patterns.singleton import Singleton
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MONGODB_URI
from app.services.utils import Action, Log, ConfigThreshold, Alert
from app.repository.config_threshold import ThresholdRepository

class BaseNotifier(Singleton, Observer):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.subscribers = SubscriberRepository.get_instance()
        self.logs = MongoClient(MONGODB_URI)
        self.logs = self.logs['yolofarm']
        self.logs = self.logs['logs']

    def add_subscriber(self, data):
        try:
            self.subscribers.add(data)
        except Exception as e:
            raise e

    def remove_subscriber(self, data):
        try:
            self.subscribers.remove(data)
        except Exception as e:
            raise e

    def send_email(self, content):
        if content is not None:
            channel = content._topic
            msg = MIMEMultipart()
            msg['From'] = MAIL_USERNAME
            recvs = [x['email'] for x in self.subscribers.get_all_by_channel(channel)]
            if not recvs:
                return
            msg['To'] = ", ".join(recvs)
            msg['Subject'] = 'Adafruit Notification'
            body = str(content)
            msg.attach(MIMEText(body, 'plain'))
            try:
                with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
                    if MAIL_USE_TLS:
                        server.starttls()
                    if MAIL_USE_SSL:
                        server.starttls()

                    server.login(MAIL_USERNAME, MAIL_PASSWORD)
                    server.send_message(msg)
                    print(f"Email sent to {msg['To']}")
            except Exception as e:
                print(f"Failed to send email: {e}")

    def store_log(self, data):
        try:
            self.logs.insert_one({
                'content': str(data),
                'timestamp': data._timestamp,
            })
        except Exception as e:
            raise e
    def update(self, data):
        pass

class BoundaryNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()
        self.threshold_repository = ThresholdRepository()

    def update(self, data: Log):
        if type(data) is not Log:
            return
        alert = None
        min = self.threshold_repository.get_threshold(data._topic).get('lower')
        max = self.threshold_repository.get_threshold(data._topic).get('upper')
        if min > data._value or max < data._value:
            alert = Alert(data._topic, data._value)
        t = Thread(target=self.send_email, args=(alert,))
        t.start()
        t.join()

class ActionNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()

    def update(self, data: Action):
        if type(data) is not Action:
            return
        t = Thread(target=self.send_email, args=(data,))
        t.start()
        self.store_log(data)

class ThresholdNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()

    def update(self, data: ConfigThreshold):
        if type(data) is not ConfigThreshold:
            return
        t = Thread(target=self.send_email, args=(data,))
        t.start()
        self.store_log(data)
    