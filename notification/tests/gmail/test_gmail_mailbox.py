from unittest.mock import MagicMock

from notification.mail.gmail.mailbox import GmailMailbox


def test_send_no_creds():
    mailbox = GmailMailbox(MagicMock(), MagicMock())

    mailbox._send()
    mailbox.logger.error.assert_called_once_with(
        "Can't send GMAIL message. No credentials or message empty."
    )
