import os

from flask import Flask

from utils.Database import Database

from config import config_by_name

FLASK_LEVEL = os.environ.get("FLASK_LEVEL", "dev")

database = Database()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name[FLASK_LEVEL])
    database.initDatabase(app)
    return app