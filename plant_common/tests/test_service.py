from unittest.mock import MagicMock, patch

import pytest

from plant_common.service import BaseService


@patch("plant_common.service.sleep")
def test_run_not_implemented(_):
    client = MagicMock()
    service = BaseService(name="test", logger=MagicMock(), client=client)

    with pytest.raises(NotImplementedError):
        service.run()


@patch("plant_common.service.schedule")
@patch("plant_common.service.sleep")
def test_run(mock_sleep, mock_schedule):
    client = MagicMock()
    service = BaseService(name="test", logger=MagicMock(), client=client)
    service._setup_mqtt = MagicMock()
    service._setup_scheduled_jobs = MagicMock()
    service.shutdown = MagicMock()
    service.shutdown.__bool__ = MagicMock(side_effect=[False, True])

    service.run()

    service._setup_mqtt.assert_called_once()
    service._setup_scheduled_jobs.assert_called_once()
    mock_sleep.assert_called_once()
    assert mock_schedule.run_pending.call_count == 2


@patch("plant_common.service.sleep")
def test_setup_mqtt(_):
    client = MagicMock()
    service = BaseService(name="test", logger=MagicMock(), client=client)
    service._subscribe = MagicMock()

    service._setup_mqtt()

    service._subscribe.assert_called_once()
