from unittest.mock import MagicMock, call, patch

import gphoto2 as gp

from plant_common.mqtt.model import LedState

from camera.mock_photocamera import DummyCamera
from camera.service import Service


@patch.dict("camera.service.config", {"CAMERA": True})
@patch("camera.service.sleep")
@patch("camera.service.Camera")
def test_handle_make_picture(mock_camera: MagicMock, mock_sleep: MagicMock):
    client = MagicMock()
    service = Service(name="test", logger=MagicMock(), client=client)
    service.camera.capture = MagicMock(return_value="picture_name")

    led_state = LedState.build(state=True)

    service.handle_make_picture(MagicMock(), "", led_state)

    mock_sleep.assert_called_once()
    service.camera.capture.assert_called_once()
    service.client.publish.assert_called()
    assert service.client.publish.call_count == 2


@patch("camera.service.sleep")
def test_dummy_camera(_, service: Service):

    led_state = LedState.build(state=True)

    service.handle_make_picture(MagicMock(), "", led_state)

    assert isinstance(service.camera, DummyCamera)
    service.logger.info.assert_called_once()


@patch("camera.service.sleep")
def test_pre_run_errror(_, service: Service):
    service.camera.set_capture_target = MagicMock(side_effect=Exception)
    service.handle_camera_error = MagicMock()

    service._pre_run()

    service.handle_camera_error.assert_called_once()


@patch("camera.service.sleep")
def test_picture_error(_, service: Service):
    service.camera.capture = MagicMock(side_effect=Exception)
    service.handle_camera_error = MagicMock()

    service.handle_make_picture(MagicMock(), MagicMock(), LedState.build(state=True))

    service.handle_camera_error.assert_called_once()


@patch("camera.service.sleep")
def test_handle_camera_error_already_registered(_, service: Service):
    service.camera_error_alert_timer = MagicMock()

    service.handle_camera_error(MagicMock(), MagicMock(), MagicMock())

    service.client.publish.assert_not_called()


@patch("camera.service.sleep")
def test_handle_camera_error_new(_, service: Service):
    service.camera_error_alert_timer = MagicMock()
    service.camera_error_alert_timer.is_counting = MagicMock(return_value=False)

    service.handle_camera_error("msg", "topic", MagicMock())

    service.client.publish.assert_called_once()


@patch("camera.service.sleep")
def test_handle_make_picture_focus_error(_, service: Service):
    service.camera.capture = MagicMock(
        side_effect=100 * [gp.GPhoto2Error(code=gp.GP_ERROR_CAMERA_BUSY)]
    )
    service.handle_camera_error = MagicMock()
    expected_args = [call(f"Attempt {i+1}/5. Couldn't focus.") for i in range(4)]
    service.handle_make_picture(
        MagicMock(), MagicMock(), message=LedState.build(state=True)
    )

    service.client.publish.assert_called_once()
    service.handle_camera_error.assert_called_once()
    assert service.logger.warning.call_args_list == [
        call("MOCK camera device selected"),
        *expected_args,
    ]


@patch("camera.service.sleep")
def test_handle_make_picture_focus_error_resolved(_, service: Service):
    service.camera.capture = MagicMock(
        side_effect=[
            gp.GPhoto2Error(code=gp.GP_ERROR_CAMERA_BUSY),
            gp.GPhoto2Error(code=gp.GP_ERROR_CAMERA_BUSY),
            "FILE.jpg",
        ]
    )

    service.handle_make_picture(
        MagicMock(), MagicMock(), message=LedState.build(state=True)
    )

    service.client.publish.assert_called()
    assert service.logger.warning.call_args_list == [
        call("MOCK camera device selected"),
        call("Attempt 1/5. Couldn't focus."),
        call("Attempt 2/5. Couldn't focus."),
    ]
    assert service.client.publish.call_count == 2
