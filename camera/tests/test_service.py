from unittest.mock import MagicMock, patch

from plant_common.model import LedState

from camera.service import Service
from camera.mock_photocamera import DummyCamera


@patch.dict("camera.service.config", {"CAMERA": True})
@patch("camera.service.sleep")
@patch("camera.service.Camera")
def test_handle_make_picture(mock_camera: MagicMock, mock_sleep: MagicMock):
    client = MagicMock()
    service = Service(name="test", logger=MagicMock(), client=client)

    led_state = LedState.build(state=True)

    service.handle_make_picture(MagicMock(), "", led_state)

    mock_sleep.assert_called_once()
    service.camera.capture.assert_called_once()


@patch.dict("camera.service.config", {"CAMERA": False})
@patch("camera.service.sleep")
def test_dummy_camera(mock_sleep: MagicMock):
    client = MagicMock()
    service = Service(name="test", logger=MagicMock(), client=client)

    led_state = LedState.build(state=True)

    service.handle_make_picture(MagicMock(), "", led_state)

    assert isinstance(service.camera, DummyCamera)
    mock_sleep.assert_called_once()
