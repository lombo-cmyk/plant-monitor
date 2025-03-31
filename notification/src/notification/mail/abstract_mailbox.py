from logging import Logger

from notification.mail.model import Message


class AbstractMailbox:
    def __init__(self, message: Message, logger: Logger):
        self.logger = logger
        self.message_content = message

    def send(self):
        try:
            self._prepare()
            self._send()
        except NotImplementedError:
            raise
        except Exception:
            self.logger.exception(
                f"Failed to send message: {self.message_content.topic}"
            )

    def _prepare(self):
        raise NotImplementedError

    def _send(self):
        raise NotImplementedError
