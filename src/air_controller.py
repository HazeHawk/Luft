
import sys

from PySide2.QtWidgets import QApplication, QWidget

from src.air_view import AirView
from src.air_model import AirModel


class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.widget = QWidget()

        ui = AirView()
        ui.setupUi(self.widget)
        print("lulus")




    def run(self):
        print("Derpiger run")
        self.widget.show()
        print("Derpiger run")



