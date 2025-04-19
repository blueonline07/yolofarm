from app.patterns.observer import Observer
import smtplib
from threading import Thread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.utils import Decision
from app.repository.subcriber import SubscriberRepository
from app.patterns.singleton import Singleton
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL
from app.services.utils import Control

class BaseNotifier(Singleton, Observer):

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.subcribers = SubscriberRepository.get_instance()

    def add_subcriber(self, data):
        try:
            self.subcribers.add(data)
        except Exception as e:
            raise e

    def send_email(self, content):
        if content is not None:
            channel = content._topic
            msg = MIMEMultipart()
            msg['From'] = MAIL_USERNAME
            recvs = [x['email'] for x in self.subcribers.get_all_by_channel(channel)]
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
    def update(self, data):
        pass

class BoundaryNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()

    def update(self, data):
        alert = Decision.simple(data['topic'], float(data['value']))
        if alert is None:
            return
        t = Thread(target=self.send_email, args=(alert,))
        t.start()
        
class ActionNotifier(BaseNotifier):
    def __init__(self):
        super().__init__()

    def update(self, data):
        topic = data['topic']
        if topic not in ['fan', 'pump', 'light']:
            return
        action = Control(topic, float(data['value']))
        t = Thread(target=self.send_email, args=(action,))
        t.start()


    