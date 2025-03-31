from unittest.mock import MagicMock, patch

from notification.service import Service


@patch.dict(
    "notification.service.config", {"MAILBOX": "GMAIL", "RECEIVERS": "hamster@goo.com"}
)
@patch("builtins.exit")
def test_pre_run_gmail_error(mock_exit: MagicMock):
    service = Service("test_service", MagicMock(), MagicMock())

    service._pre_run()

    mock_exit.assert_called_once_with(1)


@patch.dict("notification.service.config", {"MAILBOX": "SNS"})
@patch("builtins.exit")
def test_pre_run_sns_error(mock_exit: MagicMock):
    service = Service("test_service", MagicMock(), MagicMock())

    service._pre_run()

    mock_exit.assert_called_once_with(1)


@patch.dict(
    "notification.service.config",
    {"MAILBOX": "GMAIL", "RECEIVERS": "hamster@goo.com", "SENDER": "someone"},
)
@patch("builtins.exit")
def test_pre_run_success(mock_exit: MagicMock):
    service = Service("test_service", MagicMock(), MagicMock())

    service._pre_run()

    mock_exit.assert_not_called()
