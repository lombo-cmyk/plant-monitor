from unittest.mock import MagicMock, patch
from freezegun import freeze_time


from camera.photocamera import Camera


@freeze_time("2022-10-14 03:21:37")
def test_save():
    camera = Camera(MagicMock())

    _camera = MagicMock()
    get_mock = MagicMock()
    _camera.file_get = MagicMock(return_value=get_mock)

    camera_file_path = MagicMock()

    camera._save(_camera, camera_file_path)

    get_mock.save.assert_called_once_with("/var/pictures/2022_10_14_03_21a_37.jpg")


def test_save_error():
    """Not handled yet"""


@patch("camera.photocamera.gp")
def test_decorator(mock_gp):
    camera = Camera(MagicMock())

    camera.get_battery_level()

    mock_gp.Camera.assert_called_once()


def test_capture_error():
    """Not handled yet"""
