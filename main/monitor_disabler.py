import subprocess
from os import mkdir
from os.path import exists, expanduser

from main.monitor import Monitor
from main.monitor_status import MonitorStatus

EMPTY = ""
BASE_PATH = expanduser("~")
SETTINGS_PATH = f"{BASE_PATH}/.monitor_disabler"


class MonitorDisabler():

    def __init__(self) -> None:
        self.status = self.__check_status()

    def start(self):
        bash_command = "xrandr | grep ' connected ' | awk '{ print$1 }'"
        monitor_bytes, error = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE, shell=True).communicate()
        if not error:
            monitor_strings = self._get_monitors_from_bytes(monitor_bytes)
            allowed_monitors = [Monitor(x) for x in monitor_strings if self.__is_contain(x)]

    def _get_monitors_from_bytes(self, monitor_byte):
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
            return MonitorStatus.NORMAL_MODE
        else:
            mkdir(SETTINGS_PATH)
            return MonitorStatus.FIRST_START


a = MonitorDisabler()
a.start()
