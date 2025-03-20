from plant_common.logger import get_logger

from camera.service import Service

logger = get_logger("camera")


def run():
    service = Service("camera", logger)
    service.run()
