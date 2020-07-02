
import sys
from datetime import datetime

import pymongo as pm

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import *

from src.air_view import AirView
from src.air_model import AirModel
from src.config import Configuration
import folium

_cfg = Configuration()
logger = _cfg.LOGGER

class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.widget = QWidget()

        self._ui = AirView()
        self._ui.setupUi(self.widget)

        self._homeDateStart = self._ui.homeDateEditStart.date()
        self._homeDateEnd = self._ui.homeDateEditEnd.date()
        self._ui.homeDateEditStart.dateChanged.connect(self.setHomeDateStart)
        self._ui.homeDateEditEnd.dateChanged.connect(self.setHomeDateEnd)

        self.model = AirModel()
        self.model.test_model()

        timeframe = [datetime.fromisoformat("2020-01-01 12:00:00"), datetime.fromisoformat("2020-01-01 13:00:00")]

        result = self.model.find_sensors_by(timeframe=timeframe)

        for item in result[:100]:
            #print(item["location"]["coordinates"])
            long, lat = item["location"]["coordinates"]
            self.setFoliumCircle(lat, long, "test")

    def test(self):
        sensors = self.model.get_sensors()
        jan = datetime(year=2020, month=1, day=1)

        cursor = self.model.find_sensors_by(day=jan)

        print(cursor.explain())

    def create_index(self):
        collection = self.model.get_sensors()
        # collection.create_index(keys=("timestamp",pm.ASCENDING), background=True)
        pass

    def run(self):

        self.widget.show()


    def setFoliumCircle(self, lat:float, long:float, popup:str):
        folium.Circle(
            location=[lat, long],
            radius=20,
            popup=popup,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(self._ui.m)

        self._ui.homeWidgetMap.setHtml(self._ui.saveFoliumToHtml().getvalue().decode())

        self._ui.homeWidgetMap.update()

    def setHomeDateStart(self):
        logger.debug(self._ui.homeDateEditStart.date())
        self._homeDateStart = self._ui.homeDateEditStart.date()

    def getHomeDateStart(self):
        return self._homeDateStart

    def setHomeDateEnd(self):
        logger.debug(self._ui.homeDateEditEnd.date())
        self._homeDateEnd = self._ui.homeDateEditEnd.date()

    def getHomeDateEnd(self):
        return self._homeDateEnd

    def setLabelMedian(self, median: str):
        self._ui.homeLabelMedian.setText(median)

    def setLabelMaximum(self, maximum: str):
        self._ui.homeLabelMaximal.setText(maximum)

    def setLabelMinimum(self, minimum: str):
        self._ui.homeLabelMinimal.setText(minimum)

    def setLabelAverag(self, average:str):
        self._ui.homeLabelAverage.setText(average)

    def setLabelSensorCount(self, sensorCount: str):
        self._ui.homeLabelSencorCount.setText(sensorCount)