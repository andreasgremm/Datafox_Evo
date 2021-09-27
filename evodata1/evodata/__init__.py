import os
from dotenv import load_dotenv
from flask import Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
app = Flask(__name__)
app.config.from_object("config")
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    INFLUXDB_HOST=os.getenv('INFLUXDB_HOST'),
    INFLUXDB_USER=os.getenv('INFLUXDB_USER'),
    INFLUXDB_PASSWORD=os.getenv('INFLUXDB_PASSWORD'),
    EVODATA_IP=os.getenv('EVODATA_IP'),
    DEBUG_HOST=os.getenv('DEBUG_HOST'),
)

from evodata import sichten
