
import sys

from PySide2.QtWidgets import QApplication, QWidget

from src.air_view import AirView
from src.air_model import AirModel
from src.config import Configuration

_cfg = Configuration()
logger = _cfg.LOGGER

class AirController(object):

    def __init__(self):
        self.app = QApplication(sys.argv)

        self.widget = QWidget()

        ui = AirView()
        ui.setupUi(self.widget)

        model = AirModel()




    def run(self):

        self.widget.show()




