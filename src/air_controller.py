
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtGui import *

from src.air_view import AirView
from src.air_model import AirModel
import folium


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

        print("lulus")


    def run(self):
        print("Derpiger run")
        self.widget.show()

        folium.CircleMarker(
            location=[48.77915707462204, 9.175987243652344],
            radius=50,
            popup='Test',
            color='#3186cc',
            fill=True,
            fill_color='#3186cc'
        ).add_to(self._ui.m)

        self._ui.homeWidgetMap.setHtml(self._ui.saveFoliumToHtml().getvalue().decode())

        self._ui.homeWidgetMap.update()
        print("Derpiger run")

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