from plant_common.logger import get_logger

from notification.service import Service

logger = get_logger("notification")


if __name__ == "__main__":
    service = Service("notification", logger)
    service.run()
