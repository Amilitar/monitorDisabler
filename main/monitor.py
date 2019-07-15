from main.enumerations.monitor_status import MonitorStatus


class Monitor:
    def __init__(self, monitor_str) -> None:
        self.is_primary = self.get_primary_status(monitor_str)
        self.name, self.status = self.get_options(monitor_str)

    def get_primary_status(self, monitor_str):
        return "primary" in monitor_str

    def get_options(self, monitor_str):
        options = monitor_str.split(" ")
        return options[0], self.__get_status_from_string(options[1])

    def __get_status_from_string(self, status_str):
        return MonitorStatus(status_str)
