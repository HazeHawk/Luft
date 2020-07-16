from PySide2.QtCore import QThread
from PySide2.QtCore import QThreadPool
from src.worker import Worker

class QThreadData(QThread):

    def __init__(self, target:list):
        QThread.__init__(self)
        self.target = target
        self.pool = QThreadPool()

    def __del__(self):
        self.wait()

    def run(self):
        for item in self.target:
            print("task")
            worker = Worker(item)
            self.pool.start(worker)
        self.pool.waitForDone()
        print('finish')

