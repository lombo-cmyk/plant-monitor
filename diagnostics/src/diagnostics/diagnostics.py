from diagnostics.service import Service

from plant_common.logger import get_logger


logger = get_logger("diagnostics")


def run():
    service = Service("diagnostics", logger)
    service.run()
