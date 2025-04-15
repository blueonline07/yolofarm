from app.patterns.observer import Observer
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL


class BaseNotification(Observer):
    def update(self, data):
        pass

class EmailNotification(BaseNotification):
    def __init__(self, address):
        self.address = address
        print(f"Email notification initialized for {self.address}")

    def update(self, data):
        if data is not None:
            print(f"Sending email to {self.address} with data: {data}")
            msg = MIMEMultipart()
            msg['From'] = MAIL_USERNAME
            msg['To'] = self.address
            msg['Subject'] = 'Adafruit Notification'
            body = f"haha"
            msg.attach(MIMEText(body, 'plain'))
            try:
                with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
                    if MAIL_USE_TLS:
                        server.starttls()
                    if MAIL_USE_SSL:
                        server.starttls()

                    print(MAIL_USERNAME, MAIL_PASSWORD)
                    server.login(MAIL_USERNAME, MAIL_PASSWORD)
                    server.send_message(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")

            print(f"Email sent to {self.address}")
            
    