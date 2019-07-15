import argparse
import pickle as pcl
import subprocess
from os import mkdir, remove
from os.path import exists, expanduser

from main.enumerations.app_status import AppStatus
from main.enumerations.monitor_status import MonitorStatus
from main.monitor import Monitor
from main.monitor_manager import MonitorManager

EMPTY = ""
BASE_PATH = expanduser("~")
SETTINGS_PATH = f"{BASE_PATH}/.monitor_disabler"
ALLOWED_MONITORS = f"{SETTINGS_PATH}/allowed_monitors.pcl"
WORKING_MONITORS = f"{SETTINGS_PATH}/working_monitors.pcl"


class MonitorDisabler:

    def __init__(self) -> None:
        self.__check_parameters()
        self.status = self.__check_status()
        self.allowed_monitors = self.__get_allowed_monitors()
        self.monitor_manager = MonitorManager(self.__get_working_monitors(), self.allowed_monitors)
        self.monitor_manager.smart_disable_enable()

    def __check_parameters(self):
        parameters = parser.parse_args()
        # if parameters.reset:

    def __reset(self):
        remove(SETTINGS_PATH)

    def __get_allowed_monitors(self):
        allowed_monitors = None

        bash_command = "xrandr"
        monitor_bytes, error = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE,
                                                shell=True).communicate()
        if not error:
            monitor_strings = self.__get_monitors_from_bytes(monitor_bytes)
            allowed_monitors = [Monitor(x) for x in monitor_strings if self.__is_contain(x)]

        return allowed_monitors

    @staticmethod
    def __save_monitors(path, monitors):
        try:
            with open(path, "wb") as wb:
                pcl.dump(monitors, wb)
            return monitors
        except Exception as e:
            return None

    @staticmethod
    def __get_monitors(path):
        try:
            with open(path, "rb") as rb:
                monitors = pcl.load(rb)
            return monitors
        except Exception as e:
            return None

    @staticmethod
    def __get_monitors_from_bytes(monitor_byte):
        return monitor_byte.decode("utf-8").split("\n")

    @staticmethod
    def __is_contain(source):
        statuses = ["connected", "disconnected"]
        return len([x for x in statuses if x in source]) > 0

    @staticmethod
    def __check_status():
        if exists(SETTINGS_PATH):
            return AppStatus.NORMAL_MODE
        else:
            mkdir(SETTINGS_PATH)
            return AppStatus.FIRST_START

    def __get_working_monitors(self):
        working_monitors = None
        if self.status == AppStatus.FIRST_START:
            allowed_monitors = self.__get_allowed_monitors()
            if allowed_monitors:
                working_monitors = [x for x in allowed_monitors if x.status == MonitorStatus.CONNECTED]
                self.__save_monitors(WORKING_MONITORS, working_monitors)
        else:
            working_monitors = self.__get_monitors(WORKING_MONITORS)

        return working_monitors


parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-r', default=None, help="Delete settings folder and recreate")

MonitorDisabler()
