
import sys

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

        ui = AirView()
        ui.setupUi(self.widget)

        self._homeDateStart = self._ui.homeDateEditStart.date()
        self._homeDateEnd = self._ui.homeDateEditEnd.date()
        self._ui.homeDateEditStart.dateChanged.connect(self.setHomeDateStart)
        self._ui.homeDateEditEnd.dateChanged.connect(self.setHomeDateEnd)

        model = AirModel()




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
        print(self._ui.homeDateEditStart.date())
        self._homeDateStart = self._ui.homeDateEditStart.date()

    def getHomeDateStart(self):
        return self._homeDateStart

    def setHomeDateEnd(self):
        print(self._ui.homeDateEditEnd.date())
        self._homeDateEnd = self._ui.homeDateEditEnd.date()

    def getHomeDateEnd(self):
        return self._homeDateEnd