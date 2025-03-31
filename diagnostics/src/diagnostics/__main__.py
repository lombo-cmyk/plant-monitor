from plant_common.logger import get_logger

from diagnostics.service import Service

logger = get_logger("diagnostics")

if __name__ == "__main__":
    service = Service("diagnostics", logger)
    service.run()
