from time import sleep

import cv2

from plant_common.logger import get_logger

logger = get_logger("camera")


def run():
    try:
        while True:
            cam = cv2.VideoCapture(0)
            _, image = cam.read()
            cv2.imwrite("/var/logs/testimage.jpg", image)
            cam.release()
            sleep(20)
    except Exception:
        logger.exception("Something wrong with the camera")
