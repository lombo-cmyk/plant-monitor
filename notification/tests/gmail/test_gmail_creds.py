from importlib import reload  # reload creds with singleton patched
from unittest.mock import MagicMock, mock_open, patch

from notification.mail.gmail import creds


@patch("notification.mail.gmail.creds.singleton")
@patch("builtins.open", new_callable=mock_open)
def test_creds_expired(mock_file: MagicMock, _):
    reload(creds)
    manager = creds.CredentialsManager(MagicMock())
    manager._creds = MagicMock()
    manager._creds.expired = True
    manager._creds.refresh_token = MagicMock()
    manager._creds.to_json = MagicMock(return_value="file content")

    manager._refresh_credentials()

    mock_file().write.assert_called_once_with("file content")


@patch("notification.mail.gmail.creds.singleton")
def test_creds_dont_exist(_):
    reload(creds)
    manager = creds.CredentialsManager(MagicMock())
    assert manager.creds is None


@patch("notification.mail.gmail.creds.singleton")
def test_creds_valid(_):
    reload(creds)
    manager = creds.CredentialsManager(MagicMock())
    manager._creds = MagicMock()
    assert manager.creds
