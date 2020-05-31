from main.enumeration.monitor_status import MonitorStatus


class MonitorManager:
    def __init__(self, monitor_list, allowed_monitors) -> None:
        self.allowed_monitors = allowed_monitors
        self.monitor_list = monitor_list

    @property
    def primary_monitor(self) -> list:
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
        [x.disable() for x in self.monitor_list if not x.is_primary]

    def __enable(self):
        [x.enable(self.primary_monitor) for x in self.monitor_list if not x.is_primary]
