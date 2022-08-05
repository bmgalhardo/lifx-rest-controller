import os
import logging

from app.utils import get_all_devices


class Settings:

    def __init__(self):
        self.update_period = int(os.getenv('UPDATE_PERIOD', "5"))
        self.discovery_period = int(os.getenv('DISCOVERY_PERIOD', "5"))
        self.device_list = []

    def update_device_list(self) -> None:
        """
        updates current devices in the network
        """
        devices = get_all_devices()

        logging.info(devices)
        self.device_list = devices


settings = Settings()
