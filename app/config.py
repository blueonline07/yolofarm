import os
from dotenv import load_dotenv

load_dotenv()


# MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/yolofarm")
ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")

MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = os.environ.get("MAIL_PORT", 587)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)




