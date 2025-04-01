from unittest.mock import MagicMock, patch

import pytest

from diagnostics.service import Service


@pytest.fixture()
@patch("diagnostics.service.Service.get_thermistor")
@patch("diagnostics.service.Service.get_photoresistor")
def service(_, __):
    client = MagicMock()
    logger = MagicMock()
    return Service("test", logger, client)
