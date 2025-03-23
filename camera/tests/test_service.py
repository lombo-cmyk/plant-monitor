from unittest.mock import MagicMock, patch

from plant_common.model import LedState

from camera.service import Service


@patch.dict("camera.service.config", {"CAMERA": True})
@patch("camera.service.sleep")
@patch("camera.service.Camera")
def test_handle_make_picture(mock_camera, mock_sleep):
    client = MagicMock()
    service = Service(name="test", logger=MagicMock(), client=client)

    led_state = LedState.build(state=True)

    service.handle_make_picture(MagicMock(), "", led_state)

    mock_sleep.assert_called_once()
    mock_camera.assert_called_once()
