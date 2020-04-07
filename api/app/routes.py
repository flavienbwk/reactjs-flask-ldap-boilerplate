import os

from flask_restplus import Api
from flask import Blueprint

from controller.home_controller import api as home_ns
from controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint, 
    title=os.environ.get("FLASK_SERVER_NAME"), 
    description=os.environ.get("FLASK_SERVER_DESCRIPTION"),
    version='1.0'
)

# Routes

api.add_namespace(home_ns, path='/api')
api.add_namespace(auth_ns, path='/api/auth')