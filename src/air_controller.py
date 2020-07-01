
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import *

from src.air_view import AirView
from src.air_model import AirModel
from src.config import Configuration
import folium
import datetime

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

        model = AirModel()

        #geometry = {"$box": [[9.135, 48.790], [9.220, 48.750]]}

        time = {"$gt": datetime.date(2020, 6, 10)}

        result = model.find_sensors_by(day=time)

        print(result[1])

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