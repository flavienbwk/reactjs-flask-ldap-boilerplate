import os

from flask_restplus import Api
from flask import Blueprint

from .controller.home_controller import api as home_ns
from .controller.auth_controller import api as auth_ns
from .controller.user_controller import api as user_ns


blueprint = Blueprint('api', __name__)
api = Api(
    blueprint, 
    title=os.environ.get("FLASK_SERVER_NAME"), 
    description=os.environ.get("FLASK_SERVER_DESCRIPTION"),
    version=os.environ.get("FLASK_API_VERSION")
)

# Routes

api.add_namespace(home_ns, path='/api')
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(user_ns, path='/api/user')