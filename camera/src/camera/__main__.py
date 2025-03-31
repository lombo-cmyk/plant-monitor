from plant_common.logger import get_logger

from camera.service import Service

logger = get_logger("camera")


if __name__ == "__main__":
    service = Service("camera", logger)
    service.run()
