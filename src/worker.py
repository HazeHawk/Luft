from PySide2.QtCore import QRunnable

class Worker(QRunnable):

    def __init__(self, task):
        super(Worker, self).__init__()
        self.task = task

    def run(self):
        self.task()

