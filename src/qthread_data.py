from PySide2.QtCore import QThread

class QThreadData(QThread):

    def __init__(self, target):
        QThread.__init__(self)
        self.target = target

    def __del__(self):
        self.wait()

    def run(self):
        self.target()

