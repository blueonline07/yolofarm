from app.patterns.observer import Observer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.services.utils import make_decision
from app.repository.subcriber import SubcriberRepository
from app.patterns.singleton import Singleton
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL

class BaseNotification(Observer):
    def update(self, data):
        pass

class EmailNotification(Singleton, BaseNotification):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.subcribers = SubcriberRepository.get_instance()
    
    def add_subcriber(self, email):
        try:
            self.subcribers.add(email)
        except Exception as e:
            raise e

    def update(self, data):
        alert = make_decision(data['topic'], float(data['value']))
        if alert is not None:
            msg = MIMEMultipart()
            msg['From'] = MAIL_USERNAME
            msg['To'] = ", ".join([x['email'] for x in self.subcribers.get_all()])
            msg['Subject'] = 'Adafruit Notification'
            body = str(alert)
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





    