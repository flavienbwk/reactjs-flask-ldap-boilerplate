
import psycopg2
from flask_sqlalchemy import SQLAlchemy

from . import Logger


class Database():

    def __init__(self, logger: Logger) -> None:
        self.database = SQLAlchemy()
        self.logger = logger

    def getDatabase(self):
        return self.database

    def isDatabaseAvailable(self, app):
        try:
            conn = psycopg2.connect(
                "host='{}' dbname='{}' user='{}' password='{}'".format(
                app.config["POSTGRES_HOST"],
                app.config["POSTGRES_DB"],
                app.config["POSTGRES_USER"],
                app.config["POSTGRES_PASSWORD"]
            ))
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False

    def initDatabase(self, app):
        self.database.init_app(app)

    def save_changes(self, data=False):
        """
        Persists data to the database.

        Don't use `data` if you .delete()
        """
        try:
            if data is not False:
                self.database.session.add(data)
            self.database.session.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            return False
