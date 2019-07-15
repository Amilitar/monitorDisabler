import pickle as pcl
import subprocess
from os import mkdir
from os.path import exists, expanduser

from main.enumerations.app_status import AppStatus
from main.enumerations.monitor_status import MonitorStatus
from main.monitor import Monitor

EMPTY = ""
BASE_PATH = expanduser("~")
SETTINGS_PATH = f"{BASE_PATH}/.monitor_disabler"
ALLOWED_MONITORS = f"{SETTINGS_PATH}/allowed_monitors.pcl"
WORKING_MONITORS = f"{SETTINGS_PATH}/working_monitors.pcl"


class MonitorDisabler:

    def __init__(self) -> None:
        self.status = self.__check_status()
        self.allowed_monitors = self.__get_allowed_monitors()
        self.working_monitors = self.__get_working_monitors()

    def __get_allowed_monitors(self):
        allowed_monitors = None
        if self.status == AppStatus.FIRST_START:
            bash_command = "xrandr"
            monitor_bytes, error = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE,
                                                    shell=True).communicate()
            if not error:
                monitor_strings = self.__get_monitors_from_bytes(monitor_bytes)
                allowed_monitors = [Monitor(x) for x in monitor_strings if self.__is_contain(x)]
                self.__save_monitors(ALLOWED_MONITORS, allowed_monitors)

        else:
            allowed_monitors = self.__get_monitors(ALLOWED_MONITORS)
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

    def __prepare_env(self):
        pass

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


a = MonitorDisabler()
