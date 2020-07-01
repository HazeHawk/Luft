

import time
import sys

from src.config import Configuration
from src.air_controller import AirController

_cfg = Configuration()
logger = _cfg.LOGGER



if __name__ == "__main__":

    startup_time = time.time()
    logger.info(f"Start Airgoogle")
    controller = AirController()
    controller.run()

    controller.setFoliumCircle(48.780, 9.175, "murks")
    controller.setFoliumCircle(48.785, 9.175, "marks")
    controller.setFoliumCircle(48.775, 9.175, "merks")
    controller.setFoliumCircle(48.780, 9.180, "mirks")
    controller.setFoliumCircle(48.780, 9.170, "morks")

    startup_time = time.time()-startup_time
    logger.info(f'Startup of AirGoogle took {startup_time}ms.')
    sys.exit(controller.app.exec_())

