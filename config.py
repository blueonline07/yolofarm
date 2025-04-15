import os
from dotenv import load_dotenv

load_dotenv()


MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/yolofarm")
ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")
