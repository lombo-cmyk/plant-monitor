from plant_common.logger import get_logger

from illumination.service import Service

logger = get_logger("illumination")


def run():
    service = Service("illumination", logger)
    service.run()
