from datetime import datetime
from unittest.mock import MagicMock

from freezegun import freeze_time

from diagnostics.service import Service


def test_evaluate_temperature_low(service: Service):
    service.evaluate_temperature(10)

    service.client.publish.assert_not_called()
    assert service.logger.method_calls == []


def test_evaluate_temperature_first_time_error(service: Service):
    service.temp_error_alert_timer = MagicMock()
    service.temp_error_alert_timer.is_counting = MagicMock(return_value=False)

    service.evaluate_temperature(100)

    service.temp_error_alert_timer.reset.assert_called_once()
    service.client.publish.assert_called_once()


def test_evaluate_temperature_another_error(service: Service):
    service.temp_error_alert_timer = MagicMock()
    service.temp_error_alert_timer.is_counting = MagicMock(return_value=True)

    service.evaluate_temperature(100)

    service.temp_error_alert_timer.reset.assert_not_called()
    service.client.publish.assert_not_called()


@freeze_time("2009-01-14 03:21:34")
def test_evaluate_temperature_first_warning(service: Service):
    service.evaluate_temperature(50)

    assert service.temp_warn_alert_start == datetime.fromisoformat(
        "2009-01-14 03:21:34"
    )


@freeze_time("2009-01-14 03:21:34")
def test_evaluate_temperature_back_to_low(service: Service):
    service.temp_warn_alert_start = datetime.fromisoformat("2009-01-14 02:21:34")

    service.evaluate_temperature(10)

    assert service.temp_warn_alert_start is None
    service.client.publish.assert_called_once()


def test_evaluate_light_low(service: Service):
    service.evaluate_brightness(10)

    assert service.logger.method_calls == []
    service.client.publish.assert_not_called()


@freeze_time("2009-01-14 03:21:34")
def test_evaluate_light_first_time_high(service: Service):
    service.evaluate_brightness(1000)

    assert service.light_alert_start == datetime.fromisoformat("2009-01-14 03:21:34")


def test_evaluate_light_still_high(service: Service):
    service.light_alert_start = MagicMock()

    service.evaluate_brightness(1000)

    service.logger.debug.assert_called_once()


@freeze_time("2009-01-14 03:21:34")
def test_evaluate_light_back_to_low(service: Service):
    service.light_alert_start = datetime.fromisoformat("2009-01-14 02:21:34")

    service.evaluate_brightness(21)
    service.client.publish.assert_called_once()
    assert service.light_alert_start is None
