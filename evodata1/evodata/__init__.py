import os
from dotenv import load_dotenv
from flask import Flask

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
app = Flask(__name__)
app.config.from_object("config")
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
)

from evodata import sichten
