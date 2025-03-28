import os.path
from logging import Logger

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from plant_common.singleton import singleton


@singleton
class CredentialsManager:
    """
    Manage credentials from token.json file created manually beforehand using web authorization.
    Fully automating this step is impossible without a service account and Google Workspace enabled.
    https://developers.google.com/identity/protocols/oauth2/service-account
    """

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self, logger: Logger):
        self._creds = None
        self.logger = logger

    @property
    def creds(self):
        if self._creds and self._creds.valid:
            return self._creds

    def get_credentials(self):
        self._read_token()
        self._refresh_credentials()

    def _read_token(self):
        if os.path.exists("/usr/src/app/token.json"):
            self._creds = Credentials.from_authorized_user_file(
                "/usr/src/app/token.json", self.SCOPES
            )
        else:
            self.logger.error(
                "Google TOKEN does not exists. Can't connect to google services."
            )

    def _refresh_credentials(self):
        if self._creds and self._creds.expired and self._creds.refresh_token:
            self._creds.refresh(Request())
            with open("/usr/src/app/token.json", "w") as token:
                token.write(self._creds.to_json())
