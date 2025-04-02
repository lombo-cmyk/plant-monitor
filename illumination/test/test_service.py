from unittest.mock import MagicMock, patch

from illumination.service import Service


@patch("illumination.service.LED")
def test_pre_run_happy(mock_led, service: Service):
    service.handle_peripheral_error = MagicMock()

    ret = service._pre_run()

    mock_led.assert_called_once()
    service.handle_peripheral_error.assert_not_called()
    assert ret is True


@patch("illumination.service.LED", side_effect=Exception)
def test_pre_run_exception(mock_led, service: Service):
    service.handle_peripheral_error = MagicMock()

    ret = service._pre_run()

    mock_led.assert_called_once()
    service.handle_peripheral_error.assert_called_once()
    assert ret is False


@patch("illumination.service.Thread")
def test_led_job_happy_path(mock_thread, service: Service):
    service.led = MagicMock()
    service._pre_run = MagicMock()

    service.led_job()

    mock_thread.assert_called_once()
    service.led.on.assert_called_once()
    service._pre_run.assert_not_called()


def test_led_job_no_led(service: Service):
    service._pre_run = MagicMock(return_value=False)

    service.led_job()

    service._pre_run.assert_called_once()
    assert service.logger.method_calls == []
