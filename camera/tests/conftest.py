from unittest.mock import MagicMock, patch

import pytest

from camera.service import Service


@pytest.fixture()
@patch.dict("camera.service.config", {"CAMERA": False})
@patch("camera.service.sleep")
def service(_):
    client = MagicMock()
    logger = MagicMock()
    return Service("test", logger, client)
