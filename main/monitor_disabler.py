import argparse
import shutil
from os import mkdir
from os.path import exists

from main.common.common_const import SETTINGS_PATH
from main.enumeration.app_status import AppStatus
from main.monitor_manager import MonitorManager


class MonitorDisabler:
    def __init__(self) -> None:
        self.__check_parameters()
        status = self.__check_status()
        self.monitor_manager = MonitorManager(status)
        self.monitor_manager.smart_disable_enable()

    def __check_parameters(self):
        parameters = parser.parse_args()
        if parameters.r:
            self.__reset()

    @staticmethod
    def __reset():
        shutil.rmtree(SETTINGS_PATH)

    @staticmethod
    def __check_status():
        if exists(SETTINGS_PATH):
            return AppStatus.NORMAL_MODE
        else:
            mkdir(SETTINGS_PATH)
            return AppStatus.FIRST_START


parser = argparse.ArgumentParser(
    description="Disable all not primary monitors, and restore in second app restart")

parser.add_argument("-r", action="store_true", help="Delete settings folder and recreate")

MonitorDisabler()
