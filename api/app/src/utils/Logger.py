import os
import logging
import logging.handlers
from slugify import slugify


PROJECT_NAME = slugify(os.environ.get("FLASK_SERVER_NAME", "project"), separator='_')

class Logger():

    def __init__(self) -> bool:
        handler = logging.handlers.WatchedFileHandler("/logs/api.{}.log".format(PROJECT_NAME))
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        root.addHandler(handler)
        self.root = root

    def debug(self, message):
        log_message = f"DEBUG: {message}"
        print(log_message, flush=True)
        self.root.debug(log_message)

    def info(self, message):
        log_message = f"INFO: {message}"
        print(log_message, flush=True)
        self.root.info(log_message)

    def warning(self, message):
        log_message = f"WARNING: {message}"
        print(log_message, flush=True)
        self.root.warning(log_message)

    def error(self, message):
        log_message = f"ERROR: {message}"
        print(log_message, flush=True)
        self.root.error(log_message)

    def critical(self, message):
        log_message = f"CRITICAL: {message}"
        print(log_message, flush=True)
        self.root.critical(log_message)
