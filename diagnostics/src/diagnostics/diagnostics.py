from plant_common.logger import get_logger

from diagnostics.service import Service

logger = get_logger("diagnostics")


def run():
    service = Service("diagnostics", logger)
    service.run()
