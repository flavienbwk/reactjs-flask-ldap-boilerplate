import os
import logging
import logging.handlers
from slugify import slugify

PROJECT_NAME = slugify(os.environ.get("FLASK_SERVER_NAME", "project"), separator='_')

class Logger():

    def __init__(self) -> bool:
        logging.getLogger().addHandler(logging.StreamHandler())
        handler = logging.handlers.WatchedFileHandler("/logs/api.{}.log".format(PROJECT_NAME))
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        root.addHandler(handler)
        self.root = root

    def debug(self, message):
        self.root.debug(message)

    def info(self, message):
        self.root.info(message)

    def warning(self, message):
        self.root.warning(message)

    def error(self, message):
        self.root.error(message)

    def critical(self, message):
        self.root.critical(message)
