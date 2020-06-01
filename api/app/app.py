import os

from flask import Flask

from utils.Database import Database
from utils.ApiResponse import ApiResponse

from config import config_by_name

FLASK_LEVEL = os.environ.get("FLASK_LEVEL", "dev")

database = Database()

def page_not_found(e):
    apiResponse = ApiResponse()
    apiResponse.setMessage("Page not found")
    apiResponse.setHTTPCode(404)
    return apiResponse.getResponse()

def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.config.from_object(config_by_name[FLASK_LEVEL])
    database.initDatabase(app)
    return app