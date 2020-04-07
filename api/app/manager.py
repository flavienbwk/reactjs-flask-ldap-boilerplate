import os
import json

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from routes import blueprint
from app import create_app, database

from utils.ApiResponse import ApiResponse

# Initialization

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, database.getDatabase())
manager.add_command('db', MigrateCommand)

# Commands

@manager.command
def run():
    app.run(debug=True, port=5000, host="0.0.0.0")

# System functions

@app.after_request
def after_request(response):
    response.direct_passthrough = False
    response.headers.add('Access-Control-Allow-Origin', '*')
    return ApiResponse.formatFlaskResponse(response)

if __name__ == '__main__':
    manager.run()