from illumination.service import Service

from plant_common.logger import get_logger


logger = get_logger("illumination")


def run():
    service = Service("illumination", logger)
    service.run()
