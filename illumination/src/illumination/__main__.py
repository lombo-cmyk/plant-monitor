from plant_common.logger import get_logger

from illumination.service import Service

logger = get_logger("illumination")

if __name__ == "__main__":
    service = Service("illumination", logger)
    service.run()
