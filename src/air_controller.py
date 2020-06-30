
import sys
from datetime import datetime

import pymongo as pm

from PySide2.QtWidgets import QApplication, QWidget

from src.air_model import AirModel
from src.air_view import AirView
from src.config import Configuration

_cfg = Configuration()
logger = _cfg.LOGGER

class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.widget = QWidget()

        ui = AirView()
        ui.setupUi(self.widget)

        self.model = AirModel()
        self.model.test_model()



    def test(self):
        sensors = self.model.get_sensors()
        jan = datetime(year=2020,month=1,day=1)

        cursor = self.model.find_sensors_by(day=jan)

        print(cursor.explain())

    def create_index(self):
        collection = self.model.get_sensors()
        # collection.create_index(keys=("timestamp",pm.ASCENDING), background=True)
        pass

    def run(self):

        self.widget.show()
