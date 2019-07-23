from os.path import expanduser

EMPTY = ""
BASE_PATH = expanduser("~")
SETTINGS_PATH = f"{BASE_PATH}/.monitor_disabler"
ALLOWED_MONITORS = f"{SETTINGS_PATH}/allowed_monitors.pcl"
WORKING_MONITORS = f"{SETTINGS_PATH}/working_monitors.pcl"
