import pickle as pcl
import subprocess
from subprocess import PIPE

from main.common.common_const import WORKING_MONITORS
from main.enumeration.app_status import AppStatus
from main.enumeration.monitor_status import MonitorStatus
from main.model.monitor import Monitor


class MonitorManager:
    def __init__(self, app_status) -> None:
        self.app_status = app_status
        self.allowed_monitors = self.__get_allowed_monitors()
        self.monitor_list = self.__get_monitor_list()

    @property
    def primary_monitor(self) -> Monitor:
        return [x for x in self.monitor_list if x.is_primary][0]

    @property
    def is_disabled(self) -> bool:
        return len(
            [x for x in self.allowed_monitors if
             x.status == MonitorStatus.CONNECTED and x.resolution is None]) > 0

    def smart_disable_enable(self):
        if self.is_disabled:
            self.__enable()
        else:
            self.__disable()

    def __disable(self):
        [monitor.disable() for monitor in self.monitor_list if not monitor.is_primary]

    def __enable(self):
        [monitor.enable(self.primary_monitor) for monitor in self.monitor_list if
         not monitor.is_primary]

    def __get_monitor_list(self) -> list:
        if self.app_status == AppStatus.FIRST_START:
            working_monitors = self.__get_working_monitors_from_allowed(self.allowed_monitors)
        else:
            working_monitors = self.__get_monitors(WORKING_MONITORS)
            if not working_monitors:
                working_monitors = self.__get_working_monitors_from_allowed(self.allowed_monitors)

        return working_monitors

    def __get_allowed_monitors(self) -> list:
        allowed_monitors = None

        bash_command = "xrandr"
        monitor_bytes, error = subprocess.Popen(bash_command, stdout=PIPE, shell=True).communicate()
        if not error:
            monitor_strings = self.__get_monitors_from_bytes(monitor_bytes)
            allowed_monitors = [Monitor(x) for x in monitor_strings if self.__is_contain(x)]

        return allowed_monitors

    def __get_working_monitors_from_allowed(self, allowed_monitors):
        working_monitors = None
        if allowed_monitors:
            working_monitors = [x for x in allowed_monitors if x.status == MonitorStatus.CONNECTED]
            self.__save_monitors(WORKING_MONITORS, working_monitors)
        return working_monitors

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
