import re
import subprocess
from typing import Optional

from main.enumeration.monitor_status import MonitorStatus
from main.model.resolution import Resolution

PRIMARY = "primary"

"""
HDMI-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 527mm x 296mm
DP-2 connected 1920x1080+1920+0 (normal left inverted right x axis y axis) 527mm x 296mm
"""


class Monitor:
    def __init__(self, monitor_str) -> None:
        self.resolution: Optional[Resolution] = None
        self.is_primary = self.get_primary_status(monitor_str)
        self.name, self.status = self.get_options(monitor_str)

    @staticmethod
    def get_primary_status(monitor_str):
        return PRIMARY in monitor_str

    def get_options(self, monitor_str):
        options = monitor_str.split(" ")
        self.resolution = self.__get_resolution(self.__get_resolution_str(options))
        return options[0], self.__get_status_from_string(options[1])

    @staticmethod
    def __get_status_from_string(status_str):
        return MonitorStatus(status_str)

    @staticmethod
    def __get_resolution_str(options) -> Optional[str]:
        resolution = None
        if options[2] == PRIMARY:
            resolution_str = options[3]
        else:
            resolution_str = options[2]
        resolution_match = re.match("\d{1,5}[x]\d{1,5}[+]\d{1,5}[+]\d{1,5}", resolution_str)

        if resolution_match:
            resolution = resolution_match.string

        return resolution

    @staticmethod
    def __get_resolution(resolution_str: Optional[str]):
        if resolution_str:
            resolution = Resolution()
            parameters = resolution_str.split("+")
            resolution.horizontal_position = int(parameters[1])
            resolution.vertical_position = int(parameters[2])
            parameters = parameters[0].split("x")
            resolution.horizontal_pixels_count = int(parameters[0])
            resolution.vertical_pixels_count = int(parameters[1])
            return resolution
        return None

    def disable(self):
        if not self.is_primary:
            subprocess.Popen(f"xrandr --output {self.name} --off", stdout=subprocess.PIPE,
                             shell=True).communicate()

    def enable(self, primary_monitor):
        subprocess.Popen(f"xrandr --output {self.name} --auto", stdout=subprocess.PIPE,
                         shell=True).communicate()
        position_command = self.__get_position_command(primary_monitor)
        subprocess.Popen(f"xrandr --output {self.name} {position_command} {primary_monitor.name}",
                         stdout=subprocess.PIPE,
                         shell=True).communicate()

    @staticmethod
    def __get_position_command(primary_monitor):
        if primary_monitor.resolution.horizontal_position > 0:
            return "--left-of"
        return "--right-of"
