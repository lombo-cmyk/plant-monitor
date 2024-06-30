from unittest.mock import MagicMock

import pytest

from diagnostics.diagnostics import read_thermistor


@pytest.mark.parametrize(
    "digital_reading,expected_temperature",
    [(1000, 143), (950, 96), (500, 23), (300, 6)],
)
def test_read_thermistor(digital_reading, expected_temperature):
    mock_thermistor = MagicMock()
    mock_thermistor.raw_value = digital_reading
    read_temp = read_thermistor(mock_thermistor)
    assert read_temp == expected_temperature
