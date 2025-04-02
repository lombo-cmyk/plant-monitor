from datetime import datetime
from pathlib import Path

from notification.mail.abstract_mailbox import AbstractMailbox


class MockMailbox(AbstractMailbox):

    def _prepare(self):
        pass

    def _send(self):
        filename = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.email"

        save_dir = Path("/var/logs/emails")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / Path(filename)
        with open(save_path, "w") as f:
            f.write(f"Sender: {self.message_content.sender}\n")
            f.write(f"Receivers: {self.message_content.receivers}\n")
            f.write(f"Topic: {self.message_content.topic}\n")
            f.write(f"Content: \n{self.message_content.content}\n")
        self.logger.info(f"Message {filename} saved.")
