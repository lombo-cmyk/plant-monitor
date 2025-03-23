from unittest.mock import MagicMock, patch

import pytest

from diagnostics.service import Service


@pytest.mark.parametrize(
    "digital_reading,expected_temperature",
    [(1000, 143), (950, 96), (500, 23), (300, 6)],
)
@patch("diagnostics.service.Service.get_thermistor")
@patch("diagnostics.service.Service.get_photoresistor")
def test_read_thermistor(
    mock_get_thermistor, mock_get_photo, digital_reading, expected_temperature
):
    service = Service("", MagicMock(), MagicMock())
    service.thermistor.raw_value = digital_reading

    read_temp = service.read_thermistor()

    assert read_temp == expected_temperature
