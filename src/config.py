"""This is the config module.

This module contains program relevant configurations
"""

import logging


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):

    def __init__(self):

        # DEBUG Mode
        self.DEBUG = True

        #Logger
        self.LOGGER = logging.getLogger(__name__)
        format = "%(asctime)s - %(threadName)s - %(levelname)s | %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        if self.DEBUG:
            self.LOGGER.setLevel(logging.DEBUG)

        #Mongo-DB
        self.MONGO_HOST = 'hucserv193'
        self.MONGO_PORT = 8888
        self.MONGO_USERNAME = 'mongoadmin'
        self.MONGO_PASSWORD = 'Ze3cr1t!'







