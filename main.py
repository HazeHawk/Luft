
import logging
import time
import sys

from src.config import Configuration
from src.air_controller import AirController

_cfg = Configuration()


if __name__ == "__main__":

    startup_time = time.time()
    logging.info(f"Start Airgoogle")

    controller = AirController()
    controller.run()

    controller.setFoliumCircle(48.77915707462204, 9.175987243652344, "murks")

    startup_time = time.time()-startup_time
    logging.info(f'Startup of AirGoogle took {startup_time}ms.')
    sys.exit(controller.app.exec_())

