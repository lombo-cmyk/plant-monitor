from unittest.mock import MagicMock, patch

from notification.mail.manager import MessageManager


@patch.dict(
    "notification.mail.manager.config", {"SENDER": "sender@mail", "MAILBOX": "boo"}
)
@patch("notification.mail.manager.MAILBOX_CLS")
@patch("notification.mail.manager.Message")
def test_send(mock_message, mock_mailbox_cls):
    sender = MagicMock()
    mock_mailbox = MagicMock(return_value=sender)
    mock_mailbox_dict = {"boo": mock_mailbox}
    mock_mailbox_cls.__getitem__.side_effect = mock_mailbox_dict.__getitem__

    manager = MessageManager(
        to=["receiver"],
        topic="test_topic",
        content="test_content",
        severity="NONE",
        logger=MagicMock(),
    )
    manager.send()

    mock_mailbox.assert_called_once()
    sender.send.assert_called_once()
