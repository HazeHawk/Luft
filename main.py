

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
   # controller.run()
    startup_time = time.time()-startup_time
    logger.info(f'Startup of AirGoogle took {startup_time}ms.')
    #sys.exit(controller.app.exec_())

