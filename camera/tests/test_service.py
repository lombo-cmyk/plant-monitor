from unittest.mock import MagicMock, patch

from plant_common.model import LedState

from camera.service import Service


@patch("camera.service.cv2")
@patch("camera.service.sleep")
@patch("camera.service.config", autospec={"CAMERA": True})
def test_handle_led_state(mock_config, mock_sleep, mock_cv):
    led_state = LedState.build(state=True)
    client = MagicMock()
    service = Service("test", logger=MagicMock(), client=client)

    service.handle_led_state(MagicMock(), "", led_state)

    mock_sleep.assert_called_once()
    mock_cv.assert_not_called()
