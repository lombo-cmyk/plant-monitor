from unittest.mock import MagicMock

import pytest

from illumination.service import Service


@pytest.fixture()
def service():
    client = MagicMock()
    logger = MagicMock()
    return Service("test", logger, client)
