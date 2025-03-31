from unittest.mock import MagicMock

import pytest

from notification.mail.abstract_mailbox import AbstractMailbox


def test_not_implemented():
    mailbox = AbstractMailbox(MagicMock(), MagicMock())

    with pytest.raises(NotImplementedError):
        mailbox.send()
