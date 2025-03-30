import base64
from email.message import EmailMessage
from logging import Logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from plant_common.message.model import Message

from notification.mail.abstract_mailbox import AbstractMailbox
from notification.mail.gmail.creds import CredentialsManager


class GmailMailbox(AbstractMailbox):
    def __init__(self, message: Message, logger: Logger):
        super().__init__(message, logger)
        self.gmail_message = None
        self.creds = None

    def _prepare(self):
        self.creds = self._get_creds()
        if not self.creds:
            self.logger.error("Can't prepare GMAIL message. No credentials.")
            return

        email = EmailMessage()
        email.set_content(self.message_content.content)

        email["To"] = self.message_content.receivers
        email["From"] = self.message_content.sender
        email["Subject"] = self.message_content.topic

        encoded_message = base64.urlsafe_b64encode(email.as_bytes()).decode()

        self.gmail_message = {"raw": encoded_message}

    def _send(self):
        if not self.creds or not self.gmail_message:
            self.logger.error(
                "Can't send GMAIL message. No credentials or message empty."
            )
            return

        service = build("gmail", "v1", credentials=self.creds)
        sent_message = None
        try:
            sent_message = (
                service.users()
                .messages()
                .send(userId="me", body=self.gmail_message)
                .execute()
            )
        except HttpError:
            self.logger.exception("Couldn't send email: ")

        if sent_message and sent_message.get("id"):
            self.logger.debug(f"Message {sent_message['id']} send")

    def _get_creds(self):
        manager = CredentialsManager(self.logger)
        manager.get_credentials()
        return manager.creds
