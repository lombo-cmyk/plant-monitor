from unittest.mock import MagicMock

from plant_common.utils.timer import Timer


def test_is_counting_false():
    timer = Timer(0, MagicMock())

    assert timer.is_counting() is False


def test_is_counting_true():
    timer = Timer(0, MagicMock())
    timer._timer = MagicMock()
    timer._timer.finished.is_set = MagicMock(return_value=False)

    assert timer.is_counting() is True
