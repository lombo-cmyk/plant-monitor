from notification.mail.abstract_mailbox import AbstractMailbox


class MockMailbox(AbstractMailbox):

    def _prepare(self):
        pass

    def _send(self):
        self.logger.info(
            f"MockedMailbox dumping message that would be sent: {self.message_content.model_dump()}"
        )
