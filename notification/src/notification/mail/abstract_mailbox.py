from logging import Logger

from notification.mail.model import Message


class AbstractMailbox:
    def __init__(self, message: Message, logger: Logger):
        self.logger = logger
        self.message_content = message

    def send(self):
        self._prepare()
        self._send()

    def _prepare(self):
        raise NotImplementedError

    def _send(self):
        raise NotImplementedError
