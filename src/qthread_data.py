from PySide2.QtCore import QThread
from PySide2.QtCore import QThreadPool
from src.worker import Worker
from src.config import Configuration

_cfg = Configuration()
logger = _cfg.LOGGER

class QThreadData(QThread):

    def __init__(self, target:list):
        QThread.__init__(self)
        self.target = target
        self.pool = QThreadPool()

    def __del__(self):
        self.wait()

    def run(self):
        for item in self.target:
            logger.debug('start ' + item.__name__)
            worker = Worker(item)
            self.pool.start(worker)
        self.pool.waitForDone()
        logger.debug('thread finished')

