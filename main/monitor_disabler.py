import pickle as pcl
import subprocess
from os import mkdir
from os.path import exists, expanduser

from main.monitor import Monitor
from main.monitor_status import MonitorStatus

EMPTY = ""
BASE_PATH = expanduser("~")
SETTINGS_PATH = f"{BASE_PATH}/.monitor_disabler"
ALLOWED_MONITORS = f"{SETTINGS_PATH}/allowed_monitors.pcl"
WORKING_MONITORS = f"{SETTINGS_PATH}/working_monitors.pcl"

class MonitorDisabler():

    def __init__(self) -> None:
        self.status = self.__check_status()
        self.working_monitors = None

    def get_allowed_monitors(self):
        if self.status == MonitorStatus.FIRST_START:
            bash_command = "xrandr | grep ' connected ' | awk '{ print$1 }'"
            monitor_bytes, error = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE,
                                                    shell=True).communicate()
            allowed_monitors = None
            if not error:
                monitor_strings = self._get_monitors_from_bytes(monitor_bytes)
                allowed_monitors = [Monitor(x) for x in monitor_strings if self.__is_contain(x)]
            return allowed_monitors
        else:
            try:
                pcl.load(ALLOWED_MONITORS)

    @staticmethod
    def _get_monitors_from_bytes(monitor_byte):
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

    def __get_working_monitors(self):
        if self.status == MonitorStatus.FIRST_START:
            allowed_monitors = self.get_allowed_monitors()
            if allowed_monitors:
                with open(SETTINGS_PATH, )
                    pcl.dump()


a = MonitorDisabler()
a.start()
