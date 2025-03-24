from unittest.mock import MagicMock, patch
from freezegun import freeze_time

from camera.photocamera import Camera


@freeze_time("2022-10-14 03:21:37")
@patch("camera.photocamera.Camera._add_timestamp_and_save")
def test_save(mock_add_timestamp_and_save):
    camera = Camera(MagicMock())

    _camera = MagicMock()
    get_mock = MagicMock()
    _camera.file_get = MagicMock(return_value=get_mock)

    camera_file_path = MagicMock()

    camera._save(_camera, camera_file_path)

    expected_path = "/var/pictures/2022_10_14_03_21_37.jpg"
    get_mock.save.assert_called_once_with(expected_path)
    mock_add_timestamp_and_save.assert_called_once_with(
        expected_path, "2022-10-14 03:21:37"
    )


def test_save_error():
    """Not handled yet"""


@patch("camera.photocamera.gp")
def test_decorator(mock_gp):
    camera = Camera(MagicMock())

    camera.get_battery_level()

    mock_gp.Camera.assert_called_once()


def test_capture_error():
    """Not handled yet"""


@patch.dict("camera.photocamera.config", {"FONT_SIZE_RATIO": 100})
@patch("camera.photocamera.Image")
@patch("camera.photocamera.ImageDraw")
def test_add_timestamp_and_save(mock_image_draw, mock_image):
    img = MagicMock()
    img.size = 100, 200
    mock_image.open = MagicMock(return_value=img)

    draw = MagicMock()
    draw.textbbox = MagicMock(return_value=(0, 0, 10, 20))
    mock_image_draw.Draw = MagicMock(return_value=draw)

    expected_x = int(100 - 10 - 0.02 * 100)
    expected_y = int(200 - 20 - 0.02 * 200)
    expected_width = int(0.003 * 200)
    expected_font_size = int(100 * 200 / 100)

    Camera._add_timestamp_and_save("/path", "timestamp")

    draw.text.assert_called_once_with(
        (expected_x, expected_y),
        "timestamp",
        fill=(255, 255, 255),
        stroke_width=expected_width,
        stroke_fill=(0, 0, 0),
        font_size=expected_font_size,
    )
