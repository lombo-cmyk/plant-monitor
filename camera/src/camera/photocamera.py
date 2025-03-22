import gphoto2 as gp
from datetime import datetime


class Camera:
    """
    Capture and save images using Canon EOS 60D camera.
    In order to keep backup files camera settings are set to save the image to SD card as well.
    """

    def __init__(self, logger):
        self.logger = logger
        self.camera = gp.Camera()
        self.camera.init()

    def set_capture_target(self):
        """
        Set camera's internal capture path.
        1 - Memory card
        0 - Internal RAM
        """
        config_widget = self.camera.get_single_config("capturetarget")
        capture_target = gp.check_result(gp.gp_widget_get_choice(config_widget, 1))
        self.logger.info(f"Setting internal camera capture target to {capture_target}")
        config_widget.set_value(capture_target)
        self.camera.set_single_config("capturetarget", config_widget)

    def get_battery_level(self) -> str:
        """
        Get battery level.
        Probably will only return 0/50/75/100%
        """
        config_widget = self.camera.get_single_config("batterylevel")
        battery_level = config_widget.get_value()
        self.logger.info(f"Battery level value: {battery_level}")

        return battery_level

    def capture(self):
        """
        Smile.
        """
        self.logger.debug("Capturing image")
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        self.logger.info(
            f"Image captured to {file_path.folder}/{file_path.name} on the camera."
        )
        self._save(file_path)

    def exit(self):
        self.camera.exit()

    def _save(self, camera_file_path):
        _name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        storage_path = f"/var/pictures/{_name}.jpg"
        self.logger.info(f"Saving new image to {storage_path}")
        camera_file = self.camera.file_get(
            camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL
        )
        camera_file.save(storage_path)
