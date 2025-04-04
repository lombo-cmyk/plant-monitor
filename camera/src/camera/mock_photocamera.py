from datetime import datetime
from random import randint


class DummyCamera:
    """
    Capture and save images using Canon EOS 60D camera.
    In order to keep backup files camera settings are set to save the image to SD card as well.
    """

    def __init__(self, logger):
        self.logger = logger
        self.logger.warning("MOCK camera device selected")

    def set_capture_target(self) -> None:
        pass

    def get_battery_level(self) -> str:
        """
        Get mocked battery level.
        """
        return str(randint(1, 100)) + "%"

    def capture(self) -> str:
        """
        Smile.
        """
        return self._save()

    def _save(self) -> str:
        """
        TODO: Create and save dummy file to disk
        """
        now = datetime.now()
        filename = now.strftime("%Y_%m_%d_%H_%M_%S")
        return filename + ".jpg"
